#!/usr/bin/env python3
"""
Test script to generate and render a Manim animation
"""

import os
import sys
import argparse
import time
from openrouter_api import OpenRouterClient
from manim_renderer import ManimRenderer

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate and render a Manim animation")
    parser.add_argument("query", help="The DSA concept to visualize")
    parser.add_argument("--api-key", default="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", 
                        help="OpenRouter API key")
    parser.add_argument("--output-dir", default="media", help="Output directory for rendered animations")
    args = parser.parse_args()
    
    # Initialize clients
    openrouter_client = OpenRouterClient(args.api_key)
    manim_renderer = ManimRenderer(args.output_dir)
    
    print(f"Generating Manim code for '{args.query}'...")
    start_time = time.time()
    
    # Generate code
    result = openrouter_client.generate_and_save(args.query)
    
    if not result["success"]:
        print(f"Error generating code: {result.get('error', 'Unknown error')}")
        return 1
    
    code_gen_time = time.time() - start_time
    print(f"Code generated successfully in {code_gen_time:.2f} seconds.")
    print(f"Saved to: {result['filename']}")
    
    # Render animation
    print(f"Rendering animation...")
    render_start = time.time()
    render_result = manim_renderer.render_animation(result["filename"])
    
    if not render_result["success"]:
        print(f"Error rendering animation: {render_result.get('error', 'Unknown error')}")
        return 1
    
    render_time = time.time() - render_start
    total_time = time.time() - start_time
    
    print(f"Animation rendered successfully in {render_time:.2f} seconds.")
    print(f"Total processing time: {total_time:.2f} seconds")
    print(f"Video file: {render_result['video_file']}")
    
    # Print the relative path for web access
    relative_path = manim_renderer.get_relative_video_path(args.query)
    print(f"Web access path: {relative_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 