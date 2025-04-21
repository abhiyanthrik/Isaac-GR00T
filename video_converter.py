import cv2
import os
import argparse
import glob
from natsort import natsorted

def create_video_from_images(image_folder, output_video_path, fps=30, img_pattern='*.png', rotate=True):
    """
    Convert a sequence of PNG images to an MP4 video with optional 90° counterclockwise rotation.
    
    Args:
        image_folder (str): Path to the folder containing PNG images
        output_video_path (str): Path where the output video will be saved
        fps (int): Frames per second for the output video
        img_pattern (str): Pattern to match image files (default: '*.png')
        rotate (bool): Whether to rotate images 90° counterclockwise
    """
    # Get all PNG files in the folder
    image_paths = glob.glob(os.path.join(image_folder, img_pattern))
    
    if not image_paths:
        print(f"No images found in {image_folder} matching pattern {img_pattern}")
        return
    
    # Sort the images naturally (e.g., 1.png, 2.png, 10.png, ...)
    image_paths = natsorted(image_paths)
    
    # Read the first image to get dimensions
    first_image = cv2.imread(image_paths[0])
    
    # Rotate the first image to get dimensions for the video
    if rotate:
        first_image = cv2.rotate(first_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    height, width, layers = first_image.shape
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 codec
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    # Counter for progress tracking
    total_images = len(image_paths)
    
    # Add each image to video
    for i, image_path in enumerate(image_paths):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Warning: Could not read image {image_path}")
            continue
        
        # Rotate the image 90 degrees counterclockwise
        if rotate:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
        out.write(img)
        
        # Print progress
        if (i + 1) % 10 == 0 or (i + 1) == total_images:
            print(f"Processing: {i + 1}/{total_images} images ({(i + 1) / total_images * 100:.1f}%)")
    
    # Release the VideoWriter
    out.release()
    
    print(f"Video saved to {output_video_path}")

def main():
    parser = argparse.ArgumentParser(description='Convert PNG images to MP4 video')
    parser.add_argument('--input', type=str, required=True, help='Input folder containing PNG images')
    parser.add_argument('--output', type=str, required=True, help='Output video path')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second (default: 30)')
    parser.add_argument('--pattern', type=str, default='*.png', help='Image file pattern (default: *.png)')
    parser.add_argument('--no-rotate', action='store_true', help='Disable 90° counterclockwise rotation')
    
    args = parser.parse_args()
    
    create_video_from_images(
        args.input, 
        args.output, 
        args.fps, 
        args.pattern, 
        rotate=not args.no_rotate
    )

if __name__ == "__main__":
    main()