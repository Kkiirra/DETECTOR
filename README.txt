# Detector

## Overview

The Detector application is designed to monitor a specified directory for new image files, insert the detected images into a pre-defined template, and print the resulting images automatically. This tool is particularly useful for automated photo processing tasks, such as event photography or photo booths.

## Features

- **Directory Monitoring**: Watches a specified directory for new image files.
- **Template Insertion**: Inserts new images into a pre-defined template.
- **Automated Printing**: Automatically sends the processed images to a printer.
- **Configurable Coordinates**: Allows setting coordinates and dimensions for the image insertion area within the template.

## Requirements

- Python 3.x
- `PIL` (Python Imaging Library)
- `watchdog` (For monitoring file system events)
- `tkinter` (For GUI)
- `subprocess` (For printing images)
- `py2app` (For building macOS applications)

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install required Python packages using pip:
   ```sh
   pip install pillow watchdog py2app
   ```
3. Download the project files and navigate to the project directory.

## Setup

1. **Application Setup**:
   The setup script (`setup.py`) is used to build the application.
   ```sh
   python setup.py py2app
   ```
   This will generate a macOS application bundle that you can run directly.

2. **Running the Script**:
   To run the script directly:
   ```sh
   python printphoto.py
   ```

## Usage

1. **Launch the Application**: Start the application by running the generated app or executing the script.
2. **Select Template**: Choose a template image into which new images will be inserted.
3. **Select Photo Directory**: Choose the directory where new photos will be monitored.
4. **Select Output Directory**: Choose the directory where the processed images will be saved.
5. **Configure Insertion Coordinates**: Set the coordinates and dimensions for the area where new images will be inserted within the template.
6. **Start Monitoring**: Click the "Start Monitoring" button to begin watching the selected directory for new images.
7. **Stop Monitoring**: Click the "Stop Monitoring" button to stop watching the directory.

## File Structure

- **printphoto.py**: Main application script.
- **setup.py**: Script for building the application using py2app.
- **alert.icns**: Icon file for the macOS application bundle (if available).
- **example.jpeg**: Example template image file.

## Example Template

The template image should have an area designated for inserting new images. Coordinates for this area can be configured through the application UI.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome. Please fork the repository and submit pull requests.

## Support

For any issues or questions, please open an issue on the GitHub repository or contact the maintainer.

---

### Sample Code Snippets

#### Setting Up the Application

```python
from setuptools import setup

APP_NAME = "Detector"
APP = ['printphoto.py']
DATA_FILES = []

OPTIONS = {
    'includes': ['PIL', 'watchdog'],
    'iconfile': 'alert.icns',
    'plist': {
        'CFBundleName': APP_NAME,
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

#### Main Script

```python
import os
import time
from tkinter import Tk, Label, Button, filedialog, StringVar, Entry

from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from datetime import datetime

class ImageHandler(FileSystemEventHandler):
    def __init__(self, template_path, update_status, app):
        self.template = Image.open(template_path)
        self.update_status = update_status
        self.app = app

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.update_status(f'Обнаружена новая фотография: {event.src_path}')
            try:
                self.app.insert_and_print_image(event.src_path)
            except Exception as e:
                self.update_status(f'Ошибка: {e}')

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Детектор")
        # (rest of the code...)
```

Enjoy using Detector! For any further assistance, please refer to the support section.
