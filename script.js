document.addEventListener('DOMContentLoaded', function() {
    // Get modal elements
    const modal = document.getElementById('video-modal');
    const closeButton = document.querySelector('.close-button');
    const youtubeFrame = document.getElementById('youtube-frame');
    const localVideo = document.getElementById('local-video');
    const loadingIndicator = document.getElementById('loading-indicator');
    const loadingText = document.getElementById('loading-text');
    
    // Get all topic buttons
    const topicButtons = document.querySelectorAll('.topic-btn');
    
    // Search elements
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    
    // Function to open modal with YouTube video
    function openVideoModal(videoId) {
        // Hide local video and show YouTube frame
        localVideo.style.display = 'none';
        youtubeFrame.style.display = 'block';
        loadingIndicator.style.display = 'none';
        
        youtubeFrame.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
        
        // Show modal with animation
        modal.style.display = 'block';
        
        // Disable body scroll when modal is open
        document.body.style.overflow = 'hidden';
        
        // Add subtle animation to content
        setTimeout(() => {
            const modalContent = document.querySelector('.modal-content');
            modalContent.style.opacity = '1';
            modalContent.style.transform = 'translateY(0)';
        }, 10);
    }
    
    // Function to open modal with local video
    function openLocalVideoModal(videoPath) {
        console.log("Opening local video with path:", videoPath);
        
        // Show local video and hide YouTube frame
        youtubeFrame.style.display = 'none';
        loadingIndicator.style.display = 'none';
        localVideo.style.display = 'block';
        
        // Clear the YouTube iframe
        youtubeFrame.src = '';
        
        // Set the video source
        localVideo.src = videoPath;
        
        // Add error handler for video loading issues
        localVideo.onerror = function() {
            console.error("Error loading video:", videoPath);
            showNotification(`Error loading video. Please try again.`, 'error');
            
            // Try to debug the video path
            fetch(`/api/debug-video-path?query=${encodeURIComponent(videoPath.split('/').slice(-2)[0])}`)
                .then(response => response.json())
                .then(data => {
                    console.log("Video path debug info:", data);
                    
                    // If we found videos in the media directory, try the first one
                    if (data.media_videos && data.media_videos.length > 0) {
                        console.log("Trying alternative video:", data.media_videos[0]);
                        localVideo.src = "/" + data.media_videos[0];
                    }
                })
                .catch(error => console.error("Debug API error:", error));
        };
        
        // Add loaded handler to confirm successful loading
        localVideo.onloadeddata = function() {
            console.log("Video loaded successfully:", videoPath);
        };
        
        // Show modal with animation
        modal.style.display = 'block';
        
        // Disable body scroll when modal is open
        document.body.style.overflow = 'hidden';
        
        // Add subtle animation to content
        setTimeout(() => {
            const modalContent = document.querySelector('.modal-content');
            modalContent.style.opacity = '1';
            modalContent.style.transform = 'translateY(0)';
        }, 10);
    }
    
    // Function to show loading in modal
    function showLoadingModal(message) {
        // Hide both video elements and show loading
        youtubeFrame.style.display = 'none';
        localVideo.style.display = 'none';
        loadingIndicator.style.display = 'flex';
        loadingText.textContent = message || 'Generating visualization...';
        
        // Show modal with animation
        modal.style.display = 'block';
        
        // Disable body scroll when modal is open
        document.body.style.overflow = 'hidden';
        
        // Add subtle animation to content
        setTimeout(() => {
            const modalContent = document.querySelector('.modal-content');
            modalContent.style.opacity = '1';
            modalContent.style.transform = 'translateY(0)';
        }, 10);
    }
    
    // Function to close modal
    function closeVideoModal() {
        const modalContent = document.querySelector('.modal-content');
        
        // Add exit animation
        modalContent.style.opacity = '0';
        modalContent.style.transform = 'translateY(20px)';
        
        // Wait for animation to complete before hiding
        setTimeout(() => {
            // Reset all video elements
            youtubeFrame.src = '';
            localVideo.pause();
            localVideo.src = '';
            
            // Hide modal and all content elements
            modal.style.display = 'none';
            youtubeFrame.style.display = 'none';
            localVideo.style.display = 'none';
            loadingIndicator.style.display = 'none';
            
            // Re-enable body scroll
            document.body.style.overflow = 'auto';
        }, 300);
    }
    
    // Add click event listeners to topic buttons with ripple effect
    topicButtons.forEach(button => {
        // Add ripple effect
        button.addEventListener('mousedown', createRipple);
        
        // Video play functionality
        button.addEventListener('click', function() {
            const videoId = this.getAttribute('data-video-id');
            
            // Add loading indicator
            this.classList.add('loading');
            
            // Reset other buttons
            topicButtons.forEach(btn => {
                if (btn !== this) {
                    btn.classList.remove('active');
                }
            });
            
            // Slight delay to show loading state
            setTimeout(() => {
                this.classList.remove('loading');
                this.classList.add('active');
                openVideoModal(videoId);
            }, 300);
        });
    });
    
    // Create ripple effect
    function createRipple(event) {
        const button = event.currentTarget;
        
        const circle = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;
        
        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${event.clientX - button.getBoundingClientRect().left - radius}px`;
        circle.style.top = `${event.clientY - button.getBoundingClientRect().top - radius}px`;
        circle.classList.add('ripple');
        
        // Remove existing ripples
        const ripple = button.querySelector('.ripple');
        if (ripple) {
            ripple.remove();
        }
        
        button.appendChild(circle);
    }
    
    // Function to check animation status
    function checkAnimationStatus(query) {
        return fetch(`/api/search-status?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error checking status: ${response.statusText}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('Error checking animation status:', error);
                return { status: 'error', message: error.message };
            });
    }
    
    // Function to poll the animation status until it's ready
    function pollAnimationStatus(query, interval = 2000, maxAttempts = 30) {
        let attempts = 0;
        
        return new Promise((resolve, reject) => {
            const checkStatus = () => {
                attempts++;
                
                checkAnimationStatus(query)
                    .then(result => {
                        if (result.status === 'ready') {
                            // Animation is ready
                            resolve(result.video_path);
                        } else if (result.status === 'error') {
                            // Error occurred
                            reject(new Error(result.message || 'An error occurred'));
                        } else if (attempts >= maxAttempts) {
                            // Max attempts reached
                            reject(new Error('Maximum polling attempts reached'));
                        } else {
                            // Still processing, update loading message
                            loadingText.textContent = `Generating visualization for "${query}"... (${attempts}/${maxAttempts})`;
                            setTimeout(checkStatus, interval);
                        }
                    })
                    .catch(error => {
                        reject(error);
                    });
            };
            
            checkStatus();
        });
    }
    
    // Enhanced search functionality
    function handleSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        if (searchTerm === '') {
            searchInput.classList.add('error');
            searchInput.focus();
            
            setTimeout(() => {
                searchInput.classList.remove('error');
            }, 500);
            
            return;
        }
        
        // Show search animation
        searchButton.classList.add('searching');
        searchButton.innerText = 'Searching...';
        
        // Check if any existing buttons match the search
        let foundMatch = false;
        
        topicButtons.forEach(button => {
            const title = button.textContent.toLowerCase();
            
            if (title.includes(searchTerm)) {
                // Highlight the matching button
                button.classList.add('matched');
                
                // Scroll to the first match
                if (!foundMatch) {
                    button.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    foundMatch = true;
                }
            } else {
                // Reset non-matching buttons
                button.classList.remove('matched');
            }
        });
        
        if (foundMatch) {
            // Reset search button
            searchButton.classList.remove('searching');
            searchButton.innerText = 'Search';
            
            // Reset highlighting after 3 seconds
            setTimeout(() => {
                topicButtons.forEach(button => {
                    button.classList.remove('matched');
                });
            }, 3000);
            
            return;
        }
        
        // If no match found in existing buttons, check if we have an animation for this query
        checkAnimationStatus(searchTerm)
            .then(result => {
                if (result.status === 'ready') {
                    // We already have a rendered animation for this query
                    searchButton.classList.remove('searching');
                    searchButton.innerText = 'Search';
                    openLocalVideoModal(result.video_path);
                } else if (result.status === 'pending') {
                    // Animation is already being generated
                    searchButton.classList.remove('searching');
                    searchButton.innerText = 'Search';
                    showLoadingModal(`Generating visualization for "${searchTerm}"...`);
                    pollAnimationStatus(searchTerm)
                        .then(videoPath => {
                            openLocalVideoModal(videoPath);
                        })
                        .catch(error => {
                            closeVideoModal();
                            showNotification(`Error: ${error.message}`, 'error');
                        });
                } else {
                    // We need to generate a new animation
                    searchButton.classList.remove('searching');
                    searchButton.innerText = 'Search';
                    showLoadingModal(`Starting visualization generation for "${searchTerm}"...`);
                    
                    // Send the request to generate the animation
                    fetch('/api/search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ query: searchTerm })
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`Error starting generation: ${response.statusText}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.status === 'processing') {
                            // The animation is being generated, poll for status
                            loadingText.textContent = `Generating visualization for "${searchTerm}"...`;
                            return pollAnimationStatus(searchTerm);
                        } else {
                            throw new Error('Failed to start animation generation');
                        }
                    })
                    .then(videoPath => {
                        // The animation is ready, display it
                        openLocalVideoModal(videoPath);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        closeVideoModal();
                        showNotification(`Error: ${error.message}`, 'error');
                    });
                }
            })
            .catch(error => {
                console.error('Error checking animation status:', error);
                searchButton.classList.remove('searching');
                searchButton.innerText = 'Search';
                showNotification(`Error: ${error.message}`, 'error');
            });
    }
    
    // Function to show notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerText = message;
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.classList.add('hide');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // Close modal when clicking the close button
    closeButton.addEventListener('click', closeVideoModal);
    
    // Close modal when clicking outside of modal content
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeVideoModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            closeVideoModal();
        }
    });
    
    // Add search button click event
    searchButton.addEventListener('click', handleSearch);
    
    // Add search input enter key event
    searchInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            handleSearch();
        }
    });
    
    // Add focus animation to search input
    searchInput.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    searchInput.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });
    
    // Initialize animations for doodles
    const doodles = document.querySelectorAll('.doodle');
    doodles.forEach(doodle => {
        doodle.style.animationDelay = `${Math.random() * 2}s`;
    });
    
    // Check for any pending visualizations on page load
    const urlParams = new URLSearchParams(window.location.search);
    const pendingQuery = urlParams.get('query');
    if (pendingQuery) {
        searchInput.value = pendingQuery;
        handleSearch();
    }
    
    // Chat functionality
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const chatResponse = document.getElementById('chat-response');
    const explanationText = document.getElementById('explanation-text');

    // Function to add a message to the chat
    function addChatMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return messageElement;
    }

    // Function to add a loading message
    function addLoadingMessage() {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'loading');
        messageElement.innerHTML = 'Thinking <div class="dots"><span></span><span></span><span></span></div>';
        chatMessages.appendChild(messageElement);
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return messageElement;
    }

    // Function to handle chat submission
    function handleChatSubmit() {
        const message = chatInput.value.trim();
        
        if (message === '') {
            chatInput.classList.add('error');
            setTimeout(() => {
                chatInput.classList.remove('error');
            }, 500);
            return;
        }
        
        // Add user message to chat
        addChatMessage(message, 'user');
        
        // Clear input
        chatInput.value = '';
        
        // Show loading indicator in chat
        const loadingMessage = addLoadingMessage();
        
        // Disable send button while processing
        sendButton.classList.add('loading');
        sendButton.disabled = true;
        
        // Send message to the actual LLM API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                message: message,
                context: 'DSA learning platform' 
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to get response from the AI');
            }
            return response.json();
        })
        .then(data => {
            // Remove loading message
            loadingMessage.remove();
            
            // Show AI response in chat
            addChatMessage(data.response, 'ai');
            
            // Check if there's a video recommendation
            if (data.videoId) {
                setTimeout(() => {
                    openVideoModal(data.videoId);
                    
                    // Add explanation to the modal if available
                    if (data.explanation) {
                        chatResponse.style.display = 'block';
                        explanationText.innerHTML = data.explanation;
                    }
                }, 500);
            }
            
            // Re-enable send button
            sendButton.classList.remove('loading');
            sendButton.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            loadingMessage.remove();
            
            // Show error message
            addChatMessage("Sorry, I encountered an error. Please try again.", 'ai');
            
            // Re-enable send button
            sendButton.classList.remove('loading');
            sendButton.disabled = false;
            
            showNotification('Error connecting to the AI service', 'error');
        });
    }

    // Generate a detailed explanation based on the topic
    function generateExplanation(topic) {
        const explanations = {
            'depth-first search (dfs)': `
                <p>Depth-First Search (DFS) is a graph traversal algorithm that explores as far as possible along each branch before backtracking.</p>
                <p>Key characteristics of DFS:</p>
                <ul>
                    <li>Uses a stack data structure (or recursion) to keep track of vertices</li>
                    <li>Explores one path completely before moving to another path</li>
                    <li>Time complexity: O(V + E) where V is vertices and E is edges</li>
                    <li>Space complexity: O(V) for the stack in worst case</li>
                </ul>
                <p>Common applications include topological sorting, finding connected components, and solving puzzles like mazes.</p>
            `,
            'linked list': `
                <p>A Linked List is a linear data structure where elements are stored in nodes, and each node points to the next node in the sequence.</p>
                <p>Key characteristics:</p>
                <ul>
                    <li>Dynamic size - can grow or shrink during execution</li>
                    <li>Efficient insertions and deletions (O(1) time if position is known)</li>
                    <li>Random access is not allowed - must traverse from beginning (O(n) time)</li>
                    <li>No wasted memory allocation</li>
                </ul>
                <p>Types include singly linked lists, doubly linked lists, and circular linked lists.</p>
            `,
            'first come first serve (fcfs)': `
                <p>First Come First Serve (FCFS) is the simplest CPU scheduling algorithm where processes are executed in the order they arrive in the ready queue.</p>
                <p>Key characteristics:</p>
                <ul>
                    <li>Non-preemptive algorithm - once a process starts, it runs until completion</li>
                    <li>Easy to implement and understand</li>
                    <li>Can cause "convoy effect" where short processes wait for long ones</li>
                    <li>Not optimal for time-sharing systems</li>
                </ul>
                <p>FCFS is often used as a baseline for comparing other scheduling algorithms.</p>
            `,
            'prim\'s algorithm': `
                <p>Prim's Algorithm is a greedy algorithm that finds a minimum spanning tree for a weighted undirected graph.</p>
                <p>Key characteristics:</p>
                <ul>
                    <li>Builds the tree one vertex at a time, starting from an arbitrary root</li>
                    <li>Always adds the edge with minimum weight that connects a vertex in the tree to a vertex outside</li>
                    <li>Time complexity: O(E log V) with binary heap implementation</li>
                    <li>Works well for dense graphs</li>
                </ul>
                <p>Applications include network design, approximation algorithms, and cluster analysis.</p>
            `,
            'stack': `
                <p>A Stack is a linear data structure that follows the Last In First Out (LIFO) principle.</p>
                <p>Key operations:</p>
                <ul>
                    <li>Push: Add an element to the top (O(1) time)</li>
                    <li>Pop: Remove the top element (O(1) time)</li>
                    <li>Peek/Top: View the top element without removing it (O(1) time)</li>
                    <li>isEmpty: Check if stack is empty (O(1) time)</li>
                </ul>
                <p>Stacks are used in function calls (call stack), expression evaluation, backtracking algorithms, and undo operations in applications.</p>
            `,
            'queue': `
                <p>A Queue is a linear data structure that follows the First In First Out (FIFO) principle.</p>
                <p>Key operations:</p>
                <ul>
                    <li>Enqueue: Add an element to the rear (O(1) time)</li>
                    <li>Dequeue: Remove an element from the front (O(1) time)</li>
                    <li>Front: View the front element without removing it (O(1) time)</li>
                    <li>isEmpty: Check if queue is empty (O(1) time)</li>
                </ul>
                <p>Queues are used in BFS traversal, job scheduling, print spooling, and handling asynchronous data transfer.</p>
            `,
            'bubble sort': `
                <p>Bubble Sort is a simple comparison-based sorting algorithm that repeatedly steps through the list and compares adjacent elements, swapping them if they're in the wrong order.</p>
                <p>Key characteristics:</p>
                <ul>
                    <li>Time complexity: O(n²) in worst and average cases</li>
                    <li>Space complexity: O(1) - in-place sorting</li>
                    <li>Stable sort - maintains relative order of equal elements</li>
                    <li>Adaptive - can be optimized to stop early if already sorted</li>
                </ul>
                <p>While not efficient for large lists, it's simple to implement and understand, making it useful for educational purposes.</p>
            `,
            'arrays': `
                <p>Arrays are a basic data structure that stores elements of the same type in contiguous memory locations.</p>
                <p>Key characteristics:</p>
                <ul>
                    <li>Fixed size (in many languages) - size is defined at creation</li>
                    <li>Random access - O(1) time to access any element</li>
                    <li>Good cache locality - elements are stored together</li>
                    <li>Not efficient for insertions/deletions in the middle - requires shifting elements</li>
                </ul>
                <p>Arrays form the foundation for many other data structures like dynamic arrays, stacks, queues, and heaps.</p>
            `
        };
        
        // Convert topic to lowercase for matching
        const lowerTopic = topic.toLowerCase();
        
        // Return explanation if found, otherwise a generic message
        return explanations[lowerTopic] || `<p>This is a video tutorial about ${topic}. Watch to learn more about this important concept in data structures and algorithms.</p>`;
    }

    // Add event listeners for chat
    sendButton.addEventListener('click', handleChatSubmit);
    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            handleChatSubmit();
        }
    });

    // Add focus animation to chat input
    chatInput.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });

    chatInput.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });

    // Update the close modal function to hide chat response
    const originalCloseVideoModal = closeVideoModal;
    closeVideoModal = function() {
        // Hide chat response
        if (chatResponse) {
            chatResponse.style.display = 'none';
        }
        
        // Call the original function
        originalCloseVideoModal();
    };
}); 