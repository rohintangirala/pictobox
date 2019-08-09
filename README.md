# pictobox

A Python script that sorts JPEG images in a directory by device make and model info found in EXIF metadata.

## How to use:

Install the `exif` module:
```sh
pip install exif
```
Run the script:
```sh
python3 pictobox.py
```

### Optional arguments:
- `--dir` or `-d`: Provide a path to another directory with images on which to run the script
- `--arrange` or `-a`: Create a `sorted-images` directory with images arranged into subdirectories by make and model

### Output:
The script outputs a formatted JSON object with the following format:
```json
{
    "<make>-<model>": [
        "<image1.jpeg>",
        "<image2.jpeg>"
    ],
    "<make>-<model>": [
        "<image1.jpeg>",
        "<image2.jpeg>"
    ],
    "Unknown": [
        "<image1.jpeg>",
        "<image2.jpeg>"
    ]
}
```

This output can be redirected to a file if desired.

### Example:
```sh
python3 pictobox.py --arrange --dir ~/Pictures > output.json
```
