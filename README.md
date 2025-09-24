# Smart Background Replacer

## Overview

Smart Background Replacer is a real-time background replacement application that uses computer vision to detect people in webcam video and replace or blur the background. Built with Python, OpenCV, and MediaPipe's Selfie Segmentation model, this application provides a user-friendly GUI for virtual meetings, video calls, or creative content creation.

## Features

- **Real-time background replacement** with static images or videos
- **Background blur** option for privacy
- **Snapshot capture** functionality to save the current frame
- **User-friendly GUI** with intuitive controls
- **Two segmentation modes**:
  - Standard edge detection (`background_replacment_gui.py`)
  - Softer edge blending for more natural transitions (`With_softer_edges.py`)

## Requirements

- Python 3.7+
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)
- NumPy (`numpy`)
- Tkinter (`tk`)
- PIL (`pillow`)

## Installation

```bash
# Clone the repository (if using git)
# git clone https://github.com/yourusername/background-replacement-mediapipe.git
# cd background-replacement-mediapipe

# Install required packages
pip install opencv-python mediapipe numpy pillow
```

## Usage

### Running the Application

You can run either version of the application:

```bash
# Standard version
python background_replacment_gui.py

# Version with softer edge transitions
python With_softer_edges.py
```

### Controls

The application provides several buttons for controlling the background replacement:

- **Select Image Background**: Choose a static image file (JPG, PNG) as background
- **Select Video Background**: Choose a video file (MP4, AVI) as dynamic background
- **Toggle Blur**: Switch between background replacement and background blur
- **Save Snapshot**: Capture and save the current frame with timestamp
- **Quit**: Close the application

## How It Works

1. **Webcam Capture**: The application captures video from your default webcam
2. **Segmentation**: MediaPipe's Selfie Segmentation model identifies the person in the frame
3. **Background Replacement**: The background is replaced with your chosen image/video or blurred
4. **Display**: The processed frame is shown in real-time in the application window

### Segmentation Modes

- **Standard Mode** (`background_replacment_gui.py`): Uses binary segmentation for clear separation between person and background
- **Soft Edge Mode** (`With_softer_edges.py`): Applies alpha blending and edge feathering for more natural-looking transitions

## Included Resources

The repository includes sample backgrounds:

- Static images: `bg1.jpg`, `bg2.jpg`, `bg3.jpg`
- Video backgrounds: `bgv2.mp4`, `bgv3.mp4`, `bgv4.mp4`

## Customization

You can easily modify the code to:

- Change the default camera by modifying the `cv2.VideoCapture(0)` parameter
- Adjust the blur intensity by changing the kernel size in `cv2.GaussianBlur(frame, (55, 55), 0)`
- Modify the segmentation threshold by changing `mask > 0.5`
- Customize the GUI appearance by modifying the color codes in the `make_button` function

## Troubleshooting

- **No camera detected**: Ensure your webcam is properly connected and not in use by another application
- **Slow performance**: Try using a lower resolution webcam or closing other resource-intensive applications
- **Poor segmentation**: Ensure you have good lighting conditions and a contrasting background

## License

[Include your license information here]

## Acknowledgements

- [MediaPipe](https://mediapipe.dev/) for the Selfie Segmentation model
- [OpenCV](https://opencv.org/) for image processing capabilities
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework
