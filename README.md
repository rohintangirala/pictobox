# Pictobox

A Python script that sorts JPEG images in a directory by device make and model info found in EXIF metadata.

Have a large directory full of pictures? Don't know whether you took them on your phone or your camera? If you answered yes to either of these questions, Pictobox could help you out.

Ideas for new features and pull requests are always welcome.

## Setup

### Run in virtual environment:

Running in a virtual environment is recommended if you do not wish to alter your main Python installation. If you do not wish to run Pictobox in a virtual environment, skip ahead to **Install required modules**.

Install virtualenv:

```sh
pip install virtualenv
```

Activate virtual environment:

```sh
source env/bin/activate
```

Deactivate virtual environment after usage:

```sh
deactivate
```

### Install required modules:

```sh
pip install -r requirements.txt
```

### Run Pictobox:

```sh
./pictobox.py
```

If you get a `Permission denied` error, make the script executable first:

```sh
chmod +x pictobox.py
```

## Optional arguments
- `--dir` or `-d`: Provide a path to another directory with images on which to run the script
- `--arrange` or `-a`: Create a directory with images arranged into subdirectories by make and model
- `--sorted` or `-s`: Specify a custom name for the directory with sorted images (Default: `sorted-images`)
- `--output` or `-o`: Specify the name of a file to which to write JSON output

Both the directory with sorted images and the output JSON file are created in the target directory of the script.

## Output
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

This output can be written to a file if desired (see optional arguments above).

## Example
```sh
./pictobox.py --arrange --dir ~/Pictures --sorted output-images --output output.json
```
