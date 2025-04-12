#!/usr/bin/env python3
"""
Script to fix the list insertion video path.
"""

import os
import shutil

def main():
    # The problematic path
    problem_path = "media/videos/list_insertion/480p15/media.mp4"
    
    # The correct path
    correct_path = "media/videos/list_insertion/480p15/list_insertion.mp4"
    
    # Check if the problematic file exists
    if os.path.exists(problem_path):
        print(f"Found problematic video file at: {problem_path}")
        
        # Ensure the target directory exists
        target_dir = os.path.dirname(correct_path)
        os.makedirs(target_dir, exist_ok=True)
        
        # Copy the file to the correct path
        try:
            shutil.copy(problem_path, correct_path)
            print(f"Successfully copied video to correct path: {correct_path}")
        except Exception as e:
            print(f"Error copying file: {str(e)}")
    
    # If the problematic file doesn't exist, check if any .mp4 files exist in the directory
    elif os.path.exists("media/videos/list_insertion/480p15"):
        print("Searching for MP4 files in directory...")
        
        dir_path = "media/videos/list_insertion/480p15"
        files = os.listdir(dir_path)
        mp4_files = [f for f in files if f.endswith(".mp4")]
        
        if mp4_files:
            print(f"Found MP4 files: {mp4_files}")
            source_file = os.path.join(dir_path, mp4_files[0])
            
            try:
                shutil.copy(source_file, correct_path)
                print(f"Copied {source_file} to {correct_path}")
            except Exception as e:
                print(f"Error copying file: {str(e)}")
        else:
            print(f"No MP4 files found in {dir_path}")
    
    # Check for other list insertion videos anywhere in the media directory
    else:
        print("Searching for list insertion videos in the media directory...")
        media_dir = "media"
        if os.path.exists(media_dir):
            for root, dirs, files in os.walk(media_dir):
                for file in files:
                    if file.endswith(".mp4") and ("list" in root.lower() or "insertion" in root.lower() or 
                                                  "list" in file.lower() or "insertion" in file.lower()):
                        source_path = os.path.join(root, file)
                        print(f"Found potential match: {source_path}")
                        
                        # Create target directory
                        os.makedirs(target_dir, exist_ok=True)
                        
                        try:
                            shutil.copy(source_path, correct_path)
                            print(f"Copied {source_path} to {correct_path}")
                            break
                        except Exception as e:
                            print(f"Error copying file: {str(e)}")
        else:
            print(f"Media directory not found: {media_dir}")
    
    # Check if we now have the file at the correct path
    if os.path.exists(correct_path):
        print(f"SUCCESS: Video file now exists at correct path: {correct_path}")
        print(f"Size: {os.path.getsize(correct_path)} bytes")
        
        # Verify the correct path
        rel_path = "media/videos/list_insertion/480p15/list_insertion.mp4"
        abs_path = os.path.abspath(rel_path)
        print(f"Relative path: {rel_path}")
        print(f"Absolute path: {abs_path}")
    else:
        print(f"ERROR: Video file still not found at correct path: {correct_path}")

if __name__ == "__main__":
    main() 