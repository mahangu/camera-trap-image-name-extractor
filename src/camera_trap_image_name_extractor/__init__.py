#!/usr/bin/env python3

"""
Camera Trap Image Name Extractor
-------------------------------
Extracts image information from camera trap directory structure.
"""

import sys
import argparse
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from datetime import datetime

def format_image_id(file_path: Path, camera_id: str) -> str:
    """Format image filename to standard format."""
    name_parts = file_path.stem.split()
    if len(name_parts) >= 6:  # Has date and time components
        year, month, day, hour, minute, second = name_parts[:6]
        formatted_date = f"{year}-{month}-{day}"
        formatted_time = f"{hour}-{minute}-{second}"
        return f"{camera_id}_{formatted_date}_{formatted_time}_JPEG"
    return file_path.name

def get_output_filename(base_filename: str) -> Path:
    """Generate output filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = Path(base_filename).stem
    suffix = Path(base_filename).suffix
    return Path(f"{name}_{timestamp}{suffix}")

def extract_camera_number(file_path: Path) -> str:
    """Extract camera number from the directory structure.
    The camera number is typically in the directory two levels up from the images."""
    try:
        # Go up two directories from the image file to get to the camera directory
        camera_dir = file_path.parent.parent.parent
        return camera_dir.name
    except Exception:
        return "unknown"

def process_directory(input_dir: Path, output_file: Path):
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        return False
        
    output_file = output_file.parent / get_output_filename(output_file.name)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(columns=['Image ID', 'Location', 'Camera', 'Species', 'Count'])
    
    total_files = sum(1 for _ in input_dir.rglob('*') 
                     if _.is_file() and not _.name.startswith('.') 
                     and _.suffix.lower() in ['.jpg', '.jpeg'])
    
    with tqdm(total=total_files, desc="Processing images") as pbar:
        for file_path in input_dir.rglob('*'):
            if (file_path.is_file() and 
                not file_path.name.startswith('.') and 
                file_path.suffix.lower() in ['.jpg', '.jpeg']):
                try:
                    rel_path = file_path.relative_to(input_dir)
                    parts = list(rel_path.parts)
                    camera_id = parts[0] if parts else "unknown"
                    species = file_path.parent.parent.name if file_path.parent.parent else "unknown"
                    count = file_path.parent.name
                    image_id = format_image_id(file_path, camera_id)
                    camera = extract_camera_number(file_path)
                    
                    df.loc[len(df)] = {
                        'Image ID': image_id,
                        'Location': str(rel_path.parent),
                        'Camera': camera,
                        'Species': species,
                        'Count': count
                    }
                    pbar.update(1)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    df = df.sort_values('Image ID')
    df.to_csv(output_file, index=False)
    print(f"Successfully saved {len(df)} images to {output_file}")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Extract image information from camera trap directory structure"
    )
    
    parser.add_argument(
        '--input-dir',
        type=Path,
        default=Path.cwd(),
        help='Input directory containing camera trap images (default: current directory)'
    )
    
    parser.add_argument(
        '--output-file',
        type=Path,
        default=Path('camera_trap_images.csv'),
        help='Output CSV file path (default: camera_trap_images_TIMESTAMP.csv in current directory)'
    )

    args = parser.parse_args()

    try:
        success = process_directory(args.input_dir, args.output_file)
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
