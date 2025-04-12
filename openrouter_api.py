import os
import json
import requests
import re
from typing import Dict, Any, Optional

class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://pinkneurons.com",  # Replace with your actual domain
            "X-Title": "Pink Neurons DSA Learning Platform"
        }
    
    def generate_manim_code(self, query: str) -> Dict[str, Any]:
        """Generate Manim code for a given DSA concept query using Gemini."""
        
        # Load the simple array visualization template as an example
        template = """
from manim import *

class SimpleArrayVisualization(Scene):
    def construct(self):
        # Title
        title = Text("Array Visualization", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Create array of values
        values = [5, 10, 15, 20, 25]
        
        # Create squares to represent each element
        squares = []
        labels = []
        
        for i, val in enumerate(values):
            square = Square(side_length=1, color=BLUE)
            square.shift(RIGHT * (i * 1.2) - RIGHT * 2)
            squares.append(square)
            
            label = Text(str(val), font_size=30).move_to(square.get_center())
            labels.append(label)
        
        # Animate creation
        self.play(*[Create(square) for square in squares])
        self.play(*[Write(label) for label in labels])
        self.wait(1)
        
        # Demonstrate operations on the array
        # Highlight a specific element
        self.play(
            squares[2].animate.set_color(YELLOW),
            labels[2].animate.set_color(RED),
            run_time=0.5
        )
        self.wait(1)
        
        # Reset colors
        self.play(
            squares[2].animate.set_color(BLUE),
            labels[2].animate.set_color(WHITE),
        )
        self.wait(1)
        
        # Conclusion
        conclusion_text = Text("Basic Array Operations", font_size=32)
        conclusion_text.next_to(title, DOWN, buff=0.5)
        self.play(Write(conclusion_text))
        self.wait(2)
"""
        
        prompt = f"""
        Write a Manim Python script to visualize the '{query}' data structure or algorithm.
        
        Important requirements:
        1. Only use standard Manim imports (from manim import *)
        2. Create a main Scene class with an informative name that demonstrates the concept visually
        3. Include clear animations that explain the concept step by step with annotations and text
        4. Keep the code simple and avoid complex features - basic animations work best
        5. Avoid using LaTeX if possible since it might not be installed
        6. If you need text, use Text() class instead of MathTex() or Tex()
        7. Start your code directly with 'from manim import *' (no markdown code blocks)
        8. Make sure any comparisons between vectors or points use appropriate methods, not direct equality checking
        9. Use standard Manim animations like Create(), Write(), FadeIn(), etc.
        
        Here's an example of a simple, working Manim animation:
        
        {template}
        
        Now create a similar animation for '{query}'. Only provide the Python code without any explanation. The code should be ready to run.
        """
        
        payload = {
            "model": "google/gemini-2.5-pro-exp-03-25:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI specialized in creating Manim animations for data structures and algorithms visualization. Output only clean, runnable Python code without any markdown formatting, explanation, or code blocks. explain everything thoroughly"
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2500
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                # Extract code from markdown code blocks if present
                manim_code = self.extract_code_from_markdown(content)
                return {
                    "success": True,
                    "code": manim_code
                }
            else:
                return {
                    "success": False,
                    "error": "No code generated in response"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_code_from_markdown(self, content: str) -> str:
        """Extract code from markdown code blocks if present."""
        # First, check if the content is enclosed in markdown code blocks
        code_block_pattern = r"```(?:python)?\s*([\s\S]*?)```"
        matches = re.findall(code_block_pattern, content)
        
        if matches:
            # Return the content of the first code block
            return matches[0].strip()
        
        # If no code blocks found but content starts with standard Manim import
        if content.strip().startswith("from manim import"):
            # Clean up any additional non-code text
            lines = content.strip().split("\n")
            code_lines = []
            in_code = False
            
            for line in lines:
                if line.startswith("from manim import") or in_code:
                    code_lines.append(line)
                    in_code = True
            
            return "\n".join(code_lines)
        
        # If nothing else matches, return the original content
        return content.strip()
    
    def save_manim_code(self, query: str, code: str) -> str:
        """Save the generated code to a Python file."""
        # Create a suitable filename from the query
        filename = f"{'_'.join(query.lower().split())}.py"
        
        # Ensure code starts with proper import
        if not code.startswith("from manim import"):
            code = "from manim import *\n\n" + code
        
        # Fix the class name to match the expected pattern for consistent video paths
        # This helps ensure Manim saves the output video with a predictable name
        class_name = ''.join(word.capitalize() for word in query.split())
        
        # Replace any class that inherits from Scene with our standardized name
        import re
        pattern = r'class\s+(\w+)\s*\(\s*Scene\s*\)'
        match = re.search(pattern, code)
        
        if match:
            original_class_name = match.group(1)
            code = code.replace(f"class {original_class_name}(Scene)", f"class {class_name}(Scene)")
            print(f"Replaced class name from '{original_class_name}' to '{class_name}' for consistent video paths")
        else:
            print(f"Warning: Could not find a class inheriting from Scene in the generated code")
        
        with open(filename, "w") as f:
            f.write(code)
        
        return filename
    
    def generate_and_save(self, query: str) -> Dict[str, Any]:
        """Generate Manim code and save it to a file."""
        result = self.generate_manim_code(query)
        
        if result["success"]:
            filename = self.save_manim_code(query, result["code"])
            return {
                "success": True,
                "filename": filename,
                "code": result["code"]
            }
        else:
            return result

# Example usage
if __name__ == "__main__":
    api_key = "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"
    client = OpenRouterClient(api_key)
    result = client.generate_and_save("merge sort")
    print(result) 
