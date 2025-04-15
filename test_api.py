#!/usr/bin/env python3
"""
Test script to directly test the API functionality
"""

import os
import time
from openrouter_api import OpenRouterClient
from manim_renderer import ManimRenderer

def main():
    # Configuration
    api_key = ""
    query = "binary tree"
    
    # Initialize components
    openrouter_client = OpenRouterClient(api_key)
    manim_renderer = ManimRenderer()
    
    # 1. Check if video already exists
    video_path = manim_renderer.get_video_path(query)
    if os.path.exists(video_path):
        print(f"Video already exists at: {video_path}")
        rel_path = manim_renderer.get_relative_video_path(query)
        print(f"Relative path: {rel_path}")
        return
    
    # 2. Create processing flag
    processing_file = f"processing_{query.replace(' ', '_')}.flag"
    with open(processing_file, 'w') as f:
        f.write(f"Started at: {time.ctime()}")
    
    try:
        # 3. Generate Manim code
        print(f"Generating code for '{query}'...")
        result = openrouter_client.generate_and_save(query)
        
        if not result["success"]:
            print(f"Failed to generate code: {result.get('error')}")
            return
        
        print(f"Code generated and saved to: {result['filename']}")
        
        # 4. Render animation
        print("Rendering animation...")
        render_result = manim_renderer.render_animation(result["filename"])
        
        if render_result["success"]:
            print(f"Animation rendered successfully!")
            print(f"Video file: {render_result.get('video_file')}")
            print(f"Web access path: {manim_renderer.get_relative_video_path(query)}")
        else:
            print(f"Failed to render animation: {render_result.get('error')}")
    
    finally:
        # 5. Clean up
        if os.path.exists(processing_file):
            os.remove(processing_file)
            print(f"Removed processing flag file")

if __name__ == "__main__":
    main() 
