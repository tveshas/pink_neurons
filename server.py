#!/usr/bin/env python3
"""
Simple HTTP server for the Pink Neurons DSA Learning Platform
"""

import http.server
import socketserver
import os
import webbrowser
import json
from urllib.parse import urlparse, parse_qs
import mimetypes
import threading
import time
from openrouter_api import OpenRouterClient
from manim_renderer import ManimRenderer
import requests

# Configure server
PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
OPENROUTER_API_KEY = "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"

# Initialize the OpenRouter client and Manim renderer
openrouter_client = OpenRouterClient(OPENROUTER_API_KEY)
manim_renderer = ManimRenderer()

# Add mime type for MP4 videos
mimetypes.add_type('video/mp4', '.mp4')

# Custom request handler
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Handle API requests
        if path.startswith("/api/"):
            self.handle_api_request(path, parsed_url)
            return
        
        # Special handling for MP4 videos in media directory
        if path.startswith("/media/") and path.endswith(".mp4"):
            # Serve the video file with appropriate headers
            try:
                file_path = os.path.join(DIRECTORY, path[1:])  # Remove leading slash
                if os.path.exists(file_path):
                    self.send_response(200)
                    self.send_header('Content-Type', 'video/mp4')
                    self.send_header('Accept-Ranges', 'bytes')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Cache-Control', 'public, max-age=3600')
                    
                    # Get file size
                    file_size = os.path.getsize(file_path)
                    self.send_header('Content-Length', str(file_size))
                    
                    self.end_headers()
                    
                    # Stream the file in chunks
                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                    return
                else:
                    print(f"Video file not found: {file_path}")
            except Exception as e:
                print(f"Error serving video: {str(e)}")
                self.send_error(500, f"Error serving video: {str(e)}")
                return
        
        # Default to serving static files for everything else
        return super().do_GET()
    
    def do_POST(self):
        # Handle POST requests
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Handle API POST requests
        if path.startswith("/api/"):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.handle_api_post_request(path, json.loads(post_data))
            return
            
        # Default response for unsupported POST requests
        self.send_response(405)  # Method Not Allowed
        self.end_headers()
    
    def handle_api_request(self, path, parsed_url):
        """Handle API GET requests"""
        query_params = parse_qs(parsed_url.query)
        
        if path == "/api/search-status":
            query = query_params.get("query", [""])[0]
            if query:
                # Check if we have a rendered video for this query
                video_path = manim_renderer.get_video_path(query)
                if os.path.exists(video_path):
                    self.send_json_response({
                        "status": "ready",
                        "video_path": manim_renderer.get_relative_video_path(query)
                    })
                else:
                    # Check if we're currently processing this query
                    processing_file = f"processing_{query.replace(' ', '_')}.flag"
                    if os.path.exists(processing_file):
                        self.send_json_response({
                            "status": "pending",
                            "message": "Animation is being generated..."
                        })
                    else:
                        self.send_json_response({
                            "status": "not_found",
                            "message": "No animation found for this query"
                        })
            else:
                self.send_error(400, "Missing query parameter")
        elif path == "/api/debug-video-path":
            query = query_params.get("query", [""])[0]
            if query:
                # Get absolute and relative paths
                abs_path = manim_renderer.get_video_path(query)
                rel_path = manim_renderer.get_relative_video_path(query)
                
                # Check if file exists 
                file_exists = os.path.exists(abs_path)
                
                # List directory contents if parent directory exists
                dir_path = os.path.dirname(abs_path)
                dir_contents = []
                if os.path.exists(dir_path):
                    dir_contents = os.listdir(dir_path)
                
                # Find existing video files in media directory
                media_path = "media/videos"
                if os.path.exists(media_path):
                    media_videos = []
                    for root, dirs, files in os.walk(media_path):
                        for file in files:
                            if file.endswith(".mp4"):
                                media_videos.append(os.path.join(root, file))
                else:
                    media_videos = ["Media directory not found"]
                
                self.send_json_response({
                    "query": query,
                    "abs_path": abs_path,
                    "rel_path": rel_path,
                    "file_exists": file_exists,
                    "dir_exists": os.path.exists(dir_path),
                    "dir_path": dir_path,
                    "dir_contents": dir_contents,
                    "media_videos": media_videos
                })
            else:
                self.send_error(400, "Missing query parameter")
        else:
            self.send_error(404, "API endpoint not found")
    
    def handle_api_post_request(self, path, data):
        """Handle API POST requests"""
        if path == "/api/search":
            query = data.get("query", "")
            if query:
                # Check if we already have a rendered video for this query
                video_path = manim_renderer.get_video_path(query)
                if os.path.exists(video_path):
                    self.send_json_response({
                        "status": "ready",
                        "video_path": manim_renderer.get_relative_video_path(query)
                    })
                    return
                
                # Create a processing flag file
                processing_file = f"processing_{query.replace(' ', '_')}.flag"
                with open(processing_file, 'w') as f:
                    f.write(f"Started at: {time.ctime()}")
                
                # Start a background thread to generate and render the animation
                threading.Thread(
                    target=self.process_search_query,
                    args=(query, processing_file)
                ).start()
                
                self.send_json_response({
                    "status": "processing",
                    "message": f"Processing search query: {query}"
                })
            else:
                self.send_error(400, "Missing query parameter")
        elif path == "/api/chat":
            # Handle chat requests to the LLM
            message = data.get("message", "")
            context = data.get("context", "")
            
            if not message:
                self.send_error(400, "Missing message parameter")
                return
            
            try:
                # Log the chat request
                print(f"Chat request: {message}")
                
                # Process the chat request with OpenRouter LLM
                response_data = self.process_chat_message(message, context)
                
                # Send the response
                self.send_json_response(response_data)
                
            except Exception as e:
                print(f"Error processing chat request: {str(e)}")
                self.send_error(500, f"Error processing chat request: {str(e)}")
        else:
            self.send_error(404, "API endpoint not found")
    
    def process_search_query(self, query, processing_file):
        """Process a search query in the background"""
        try:
            print(f"Processing search query: {query}")
            
            # Check if we already have a rendered video for this query
            video_path = manim_renderer.get_video_path(query)
            if os.path.exists(video_path):
                print(f"Animation already exists for '{query}' at: {video_path}")
                # Remove processing flag
                if os.path.exists(processing_file):
                    os.remove(processing_file)
                return
                
            # Generate Manim code using OpenRouter AI
            print(f"Generating Manim code for '{query}'...")
            result = openrouter_client.generate_and_save(query)
            
            if result["success"]:
                # Render the animation
                print(f"Rendering animation for '{query}'...")
                render_result = manim_renderer.render_animation(result["filename"])
                
                if render_result["success"]:
                    # Check if the video file exists
                    rendered_video_path = render_result.get("video_file", "")
                    print(f"Renderer reports success. Video path: {rendered_video_path}")
                    
                    if os.path.exists(rendered_video_path):
                        print(f"Successfully rendered animation for '{query}'. File exists at: {rendered_video_path}")
                        
                        # Check if the path follows the expected pattern
                        expected_path = manim_renderer.get_video_path(query)
                        if rendered_video_path != expected_path:
                            print(f"Warning: Renderer produced unexpected path. Expected: {expected_path}, Got: {rendered_video_path}")
                            
                            # Ensure the target directory exists
                            target_dir = os.path.dirname(expected_path)
                            os.makedirs(target_dir, exist_ok=True)
                            
                            # Copy the file to the expected location if different
                            try:
                                import shutil
                                shutil.copy(rendered_video_path, expected_path)
                                print(f"Copied video from {rendered_video_path} to {expected_path}")
                            except Exception as copy_error:
                                print(f"Error copying video file: {str(copy_error)}")
                    else:
                        print(f"Warning: Renderer reports success but video file not found at: {rendered_video_path}")
                        
                        # Double check if the file exists in the expected path
                        expected_path = manim_renderer.get_video_path(query)
                        if os.path.exists(expected_path):
                            print(f"Video found at expected path: {expected_path}")
                        else:
                            print(f"Video not found at expected path either: {expected_path}")
                            
                            # List directory contents
                            scene_name = os.path.basename(result["filename"]).replace(".py", "")
                            potential_dirs = [
                                f"media/videos/{scene_name}/480p15",
                                f"media/videos/{query.replace(' ', '_').lower()}/480p15"
                            ]
                            
                            for dir_path in potential_dirs:
                                if os.path.exists(dir_path):
                                    files = os.listdir(dir_path)
                                    print(f"Files in {dir_path}: {files}")
                                    
                                    # Try to find an MP4 file
                                    for file in files:
                                        if file.endswith(".mp4"):
                                            found_path = os.path.join(dir_path, file)
                                            print(f"Found video at: {found_path}")
                                            
                                            # Copy to expected path
                                            try:
                                                import shutil
                                                target_dir = os.path.dirname(expected_path)
                                                os.makedirs(target_dir, exist_ok=True)
                                                shutil.copy(found_path, expected_path)
                                                print(f"Copied video from {found_path} to {expected_path}")
                                            except Exception as copy_error:
                                                print(f"Error copying video file: {str(copy_error)}")
                    
                    # Wait for file to be fully written to disk
                    time.sleep(1)
                else:
                    print(f"Failed to render animation: {render_result.get('error', 'Unknown error')}")
            else:
                print(f"Failed to generate Manim code: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Remove processing flag
            if os.path.exists(processing_file):
                os.remove(processing_file)
                print(f"Removed processing flag: {processing_file}")
    
    def process_chat_message(self, message, context):
        """Process a chat message using OpenRouter LLM"""
        try:
            # Prepare the message payload for OpenRouter
            system_message = """You are a friendly, conversational AI assistant for a Data Structures and Algorithms (DSA) learning platform called Pink Neurons.
            
            FORMAT GUIDELINES:
            1. Write in a natural, conversational style like a helpful tutor
            2. DO NOT use markdown formatting (no ** for bold, no ``` for code blocks)
            3. Keep responses concise and easy to read
            4. Use simple formatting like dashes or numbers for lists
            5. Split longer content into short paragraphs
            
            You can answer questions about different DSA topics and provide helpful explanations.
            If a user asks about a specific DSA topic that we have a video for, provide a brief explanation and recommend the video.
            
            Available topic videos: Depth-First Search (DFS), Linked List, First Come First Serve (FCFS), Prim's Algorithm, Stack, Queue, Bubble Sort, Arrays."""
            
            payload = {
                "model": "openrouter/optimus-alpha",  # Using Claude for better formatting control
                "messages": [
                    {
                        "role": "system", 
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            # Send request to OpenRouter
            response = requests.post(
                openrouter_client.base_url,
                headers=openrouter_client.headers,
                json=payload
            )
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                
                # Check if the response mentions any of our available videos
                video_id = None
                explanation = None
                available_topics = {
                    "depth-first search": "qB7ZvdHmMqk",
                    "dfs": "qB7ZvdHmMqk",
                    "linked list": "zf1lSkE2kEQ",
                    "first come first serve": "MVrRhVskzks",
                    "fcfs": "MVrRhVskzks",
                    "prim's algorithm": "cH-E9RxyxzI",
                    "prim": "cH-E9RxyxzI",
                    "stack": "Vl1VE-YxMhc",
                    "queue": "SRWNWzwKVyw",
                    "bubble sort": "9BPJXlgTR9E",
                    "arrays": "f5bgM0fg7aY",
                    "array": "f5bgM0fg7aY"
                }
                
                # Check if response mentions any topics
                message_lower = message.lower()
                for topic, topic_id in available_topics.items():
                    if topic in message_lower:
                        video_id = topic_id
                        
                        # Format explanation for modal with proper HTML
                        explanation = f"""
                        <div class="explanation">
                            <p>Here's what you need to know about {topic}:</p>
                            {self.generate_topic_explanation(topic)}
                        </div>
                        """
                        break
                
                return {
                    "response": content,
                    "videoId": video_id,
                    "explanation": explanation
                }
            else:
                return {
                    "response": "I'm sorry, I couldn't process your request at this time. Please try again later.",
                    "videoId": None,
                    "explanation": None
                }
                
        except Exception as e:
            print(f"Error in process_chat_message: {str(e)}")
            return {
                "response": f"I encountered an error while processing your request: {str(e)}",
                "videoId": None,
                "explanation": None
            }
            
    def generate_topic_explanation(self, topic):
        """Generate HTML explanation for a topic"""
        explanations = {
            "depth-first search": """
                <p>Depth-First Search (DFS) is a graph traversal algorithm that explores as far as possible along each branch before backtracking.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Uses a stack data structure (or recursion)</li>
                    <li>Explores one path completely before moving to another</li>
                    <li>Time complexity: O(V + E) where V is vertices and E is edges</li>
                    <li>Space complexity: O(V) for the stack in worst case</li>
                </ul>
                <p>Common applications include topological sorting, finding connected components, and maze solving.</p>
            """,
            "dfs": """
                <p>Depth-First Search (DFS) is a graph traversal algorithm that explores as far as possible along each branch before backtracking.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Uses a stack data structure (or recursion)</li>
                    <li>Explores one path completely before moving to another</li>
                    <li>Time complexity: O(V + E) where V is vertices and E is edges</li>
                    <li>Space complexity: O(V) for the stack in worst case</li>
                </ul>
                <p>Common applications include topological sorting, finding connected components, and maze solving.</p>
            """,
            "linked list": """
                <p>A Linked List is a linear data structure where elements are stored in nodes, and each node points to the next node in the sequence.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Dynamic size - can grow or shrink during execution</li>
                    <li>Efficient insertions and deletions (O(1) time if position is known)</li>
                    <li>Random access is not allowed - must traverse from beginning (O(n) time)</li>
                    <li>No wasted memory allocation</li>
                </ul>
                <p>Types include singly linked lists, doubly linked lists, and circular linked lists.</p>
            """,
            "first come first serve": """
                <p>First Come First Serve (FCFS) is the simplest CPU scheduling algorithm where processes are executed in the order they arrive in the ready queue.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Non-preemptive algorithm - once a process starts, it runs until completion</li>
                    <li>Easy to implement and understand</li>
                    <li>Can cause "convoy effect" where short processes wait for long ones</li>
                    <li>Not optimal for time-sharing systems</li>
                </ul>
                <p>FCFS is often used as a baseline for comparing other scheduling algorithms.</p>
            """,
            "fcfs": """
                <p>First Come First Serve (FCFS) is the simplest CPU scheduling algorithm where processes are executed in the order they arrive in the ready queue.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Non-preemptive algorithm - once a process starts, it runs until completion</li>
                    <li>Easy to implement and understand</li>
                    <li>Can cause "convoy effect" where short processes wait for long ones</li>
                    <li>Not optimal for time-sharing systems</li>
                </ul>
                <p>FCFS is often used as a baseline for comparing other scheduling algorithms.</p>
            """,
            "prim's algorithm": """
                <p>Prim's Algorithm is a greedy algorithm that finds a minimum spanning tree for a weighted undirected graph.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Builds the tree one vertex at a time, starting from an arbitrary root</li>
                    <li>Always adds the edge with minimum weight that connects a vertex in the tree to a vertex outside</li>
                    <li>Time complexity: O(E log V) with binary heap implementation</li>
                    <li>Works well for dense graphs</li>
                </ul>
                <p>Applications include network design, approximation algorithms, and cluster analysis.</p>
            """,
            "prim": """
                <p>Prim's Algorithm is a greedy algorithm that finds a minimum spanning tree for a weighted undirected graph.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Builds the tree one vertex at a time, starting from an arbitrary root</li>
                    <li>Always adds the edge with minimum weight that connects a vertex in the tree to a vertex outside</li>
                    <li>Time complexity: O(E log V) with binary heap implementation</li>
                    <li>Works well for dense graphs</li>
                </ul>
                <p>Applications include network design, approximation algorithms, and cluster analysis.</p>
            """,
            "stack": """
                <p>A Stack is a linear data structure that follows the Last In First Out (LIFO) principle.</p>
                <h4>Key operations:</h4>
                <ul>
                    <li>Push: Add an element to the top (O(1) time)</li>
                    <li>Pop: Remove the top element (O(1) time)</li>
                    <li>Peek/Top: View the top element without removing it (O(1) time)</li>
                    <li>isEmpty: Check if stack is empty (O(1) time)</li>
                </ul>
                <p>Stacks are used in function calls (call stack), expression evaluation, backtracking algorithms, and undo operations in applications.</p>
            """,
            "queue": """
                <p>A Queue is a linear data structure that follows the First In First Out (FIFO) principle.</p>
                <h4>Key operations:</h4>
                <ul>
                    <li>Enqueue: Add an element to the rear (O(1) time)</li>
                    <li>Dequeue: Remove an element from the front (O(1) time)</li>
                    <li>Front: View the front element without removing it (O(1) time)</li>
                    <li>isEmpty: Check if queue is empty (O(1) time)</li>
                </ul>
                <p>Queues are used in BFS traversal, job scheduling, print spooling, and handling asynchronous data transfer.</p>
            """,
            "bubble sort": """
                <p>Bubble Sort is a simple comparison-based sorting algorithm that repeatedly steps through the list and compares adjacent elements, swapping them if they're in the wrong order.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Time complexity: O(n²) in worst and average cases</li>
                    <li>Space complexity: O(1) - in-place sorting</li>
                    <li>Stable sort - maintains relative order of equal elements</li>
                    <li>Adaptive - can be optimized to stop early if already sorted</li>
                </ul>
                <p>While not efficient for large lists, it's simple to implement and understand, making it useful for educational purposes.</p>
            """,
            "arrays": """
                <p>Arrays are a basic data structure that stores elements of the same type in contiguous memory locations.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Fixed size (in many languages) - size is defined at creation</li>
                    <li>Random access - O(1) time to access any element</li>
                    <li>Good cache locality - elements are stored together</li>
                    <li>Not efficient for insertions/deletions in the middle - requires shifting elements</li>
                </ul>
                <p>Arrays form the foundation for many other data structures like dynamic arrays, stacks, queues, and heaps.</p>
            """,
            "array": """
                <p>Arrays are a basic data structure that stores elements of the same type in contiguous memory locations.</p>
                <h4>Key characteristics:</h4>
                <ul>
                    <li>Fixed size (in many languages) - size is defined at creation</li>
                    <li>Random access - O(1) time to access any element</li>
                    <li>Good cache locality - elements are stored together</li>
                    <li>Not efficient for insertions/deletions in the middle - requires shifting elements</li>
                </ul>
                <p>Arrays form the foundation for many other data structures like dynamic arrays, stacks, queues, and heaps.</p>
            """
        }
        
        return explanations.get(topic.lower(), f"<p>Information about {topic} will be covered in the video.</p>")
    
    def send_json_response(self, data):
        """Send a JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

# Change to the directory containing the web files
os.chdir(DIRECTORY)

# Create the server with allow_reuse_address=True to avoid "Address already in use" errors
class TCPServerReuse(socketserver.TCPServer):
    allow_reuse_address = True

# Create the server
with TCPServerReuse(("", PORT), CustomHTTPRequestHandler) as httpd:
    print(f"Pink Neurons DSA Learning Platform")
    print(f"Server started at http://localhost:{PORT}")
    print(f"Press Ctrl+C to stop the server")
    
    # Open the browser automatically
    webbrowser.open(f"http://localhost:{PORT}")
    
    # Serve until interrupted
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.") 