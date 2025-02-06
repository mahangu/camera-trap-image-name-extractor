# Camera Trap Image Name Extractor

Extract metadata from camera trap image directories into CSV format.

## Installation

Install using pipx (recommended):
```bash
pipx install git+https://github.com/mahangu/camera-trap-image-name-extractor.git
```

## Usage

Navigate to your images directory (e.g., AllLocations/2021) and run:
```bash
camera-trap-image-name-extractor
```

This will:
1. Process all images in the current directory and subdirectories
2. Create a CSV file with timestamp (e.g., `camera_trap_images_20240206_181339.csv`)
3. Include Image ID, Location, Species, and Count information

### Options

- `--input-dir PATH`: Process a different directory (default: current directory)
- `--output-file PATH`: Specify output file name (default: camera_trap_images_TIMESTAMP.csv)
