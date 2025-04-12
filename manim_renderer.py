import os
import subprocess
import importlib.util
import sys
from typing import Dict, Any


class ManimRenderer:
    def __init__(self, output_dir="media"):
        self.output_dir = output_dir
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def render_animation(self, filename: str) -> Dict[str, Any]:
        """Render a Manim animation from a Python file."""
        # Check if file exists
        if not os.path.exists(filename):
            return {
                "success": False,
                "error": f"File {filename} does not exist"
            }
        
        try:
            # Extract the module name from the filename
            module_name = os.path.basename(filename).replace(".py", "")
            
            # Run the manim command to render the animation
            # Using -l for low quality for faster rendering during development
            # Can use -m or -h for medium or high quality in production
            # Add --disable_caching to prevent issues with cached renders
            # Add -v WARNING to reduce verbosity
            result = subprocess.run(
                [
                    "python", "-m", "manim", 
                    filename, 
                    "-o", self.output_dir,
                    "--disable_caching",
                    "-v", "WARNING",
                    "-ql"  # Low quality for fast rendering
                ],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the output to find the generated video file
            output_lines = result.stdout.split('\n')
            video_file = None
            
            for line in output_lines:
                if "Writing to file" in line and line.endswith(".mp4"):
                    video_file = line.split("Writing to file:")[-1].strip()
            
            if video_file:
                return {
                    "success": True,
                    "video_file": video_file,
                    "output": result.stdout
                }
            else:
                video_path = self.get_video_path(module_name)
                return {
                    "success": True,
                    "video_file": video_path,
                    "output": result.stdout,
                    "note": "Video file path not found in output, using default path pattern"
                }
                
        except subprocess.CalledProcessError as e:
            # If the error is related to LaTeX, try to render with --renderer=opengl
            # which doesn't require LaTeX
            if "latex failed" in str(e.stderr) or "Check your LaTeX installation" in str(e.stderr):
                try:
                    print("LaTeX not found, trying to render with OpenGL renderer...")
                    result = subprocess.run(
                        [
                            "python", "-m", "manim", 
                            filename, 
                            "-o", self.output_dir,
                            "--renderer", "opengl",
                            "--disable_caching",
                            "-v", "WARNING",
                            "-ql"  # Low quality for fast rendering
                        ],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    # Parse the output to find the generated video file
                    output_lines = result.stdout.split('\n')
                    video_file = None
                    
                    for line in output_lines:
                        if "Writing to file" in line and line.endswith(".mp4"):
                            video_file = line.split("Writing to file:")[-1].strip()
                    
                    if video_file:
                        return {
                            "success": True,
                            "video_file": video_file,
                            "output": result.stdout,
                            "note": "Rendered with OpenGL renderer (no LaTeX)"
                        }
                    else:
                        video_path = self.get_video_path(module_name)
                        return {
                            "success": True,
                            "video_file": video_path,
                            "output": result.stdout,
                            "note": "Rendered with OpenGL renderer (no LaTeX), video path not found in output"
                        }
                        
                except subprocess.CalledProcessError as e2:
                    # If that also fails, try with --renderer=cairo
                    try:
                        print("OpenGL renderer failed, trying with Cairo renderer...")
                        result = subprocess.run(
                            [
                                "python", "-m", "manim", 
                                filename, 
                                "-o", self.output_dir,
                                "--renderer", "cairo",
                                "--disable_caching",
                                "-v", "WARNING",
                                "-ql"  # Low quality for fast rendering
                            ],
                            capture_output=True,
                            text=True,
                            check=True
                        )
                        
                        # Parse the output to find the generated video file
                        output_lines = result.stdout.split('\n')
                        video_file = None
                        
                        for line in output_lines:
                            if "Writing to file" in line and line.endswith(".mp4"):
                                video_file = line.split("Writing to file:")[-1].strip()
                        
                        if video_file:
                            return {
                                "success": True,
                                "video_file": video_file,
                                "output": result.stdout,
                                "note": "Rendered with Cairo renderer (no LaTeX)"
                            }
                        else:
                            video_path = self.get_video_path(module_name)
                            return {
                                "success": True,
                                "video_file": video_path,
                                "output": result.stdout,
                                "note": "Rendered with Cairo renderer (no LaTeX), video path not found in output"
                            }
                    except subprocess.CalledProcessError as e3:
                        return {
                            "success": False,
                            "error": f"All renderers failed. Cairo error: {e3.stderr}",
                            "output": e3.stdout
                        }
                    
                    return {
                        "success": False,
                        "error": f"Rendering failed with OpenGL renderer: {e2.stderr}",
                        "output": e2.stdout
                    }
            
            return {
                "success": False,
                "error": f"Rendering failed: {e.stderr}",
                "output": e.stdout
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error: {str(e)}"
            }
    
    def get_video_path(self, query: str) -> str:
        """Get the expected path of the rendered video for a query."""
        module_name = query if isinstance(query, str) else ""
        if " " in module_name:
            module_name = "_".join(module_name.lower().split())
        return f"{self.output_dir}/videos/{module_name}/480p15/{module_name}.mp4"
    
    def get_relative_video_path(self, query: str) -> str:
        """Get the path of the rendered video relative to the web root."""
        module_name = query if isinstance(query, str) else ""
        if " " in module_name:
            module_name = "_".join(module_name.lower().split())
        return f"media/videos/{module_name}/480p15/{module_name}.mp4"


# Example usage
if __name__ == "__main__":
    renderer = ManimRenderer()
    result = renderer.render_animation("merge_sort.py")
    print(result) 