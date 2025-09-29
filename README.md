# PyQt Dual Image Viewer

This project is a PyQt5 application that allows users to view and manage two images side by side. Users can load images from specified folders, navigate through them, and save the displayed images with optional filename embedding and addtional information.

## Features

- Load images from specified folders for two display areas.
- Navigate through images using next and previous buttons.
- Save displayed images arranged horizontally or vertically into a chosen folder.
- Option to embed filenames into the saved images and additional labels.
- Supports JPG and PNG image formats.

## Project Structure

```
DualImageViewer
├── dualImgView.py              # Main entry point of the application
├── dualImgView.spec
├── file_version_info.txt
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/connyTheOne/DualImgViewMerge.git
   cd DualImageViewer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python dualImgView.py
   ```

2. Use the load buttons to select images for each display area.

3. Navigate through the images using the next and previous buttons.

4. Use the save button to save the displayed images to a chosen folder. Check the option to embed filenames or additional information if desired.


## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Third-Party
Includes PySide6 (LGPLv3). See 3rdparty-licenses/PySide6 for full LGPLv3 and GPLv3 texts and notice. No modifications were made. Source: https://code.qt.io/cgit/pyside/pyside-setup.git/
