import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import datetime

# -------------------------
# INITIAL SETUP
# -------------------------

# Initialize Mediapipe's Selfie Segmentation
# model_selection=1 is better for people farther from the camera
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segment = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

# For video backgrounds
video_cap = None

# Program state variables
bg_image = None          # Stores current background image
use_video_bg = False     # True = using a video background, False = image
blur_background = False  # If True, blur the background instead of replacing it
last_output_frame = None # Stores the latest processed frame for snapshots


# -------------------------
# FUNCTIONS
# -------------------------

def select_image_bg():
    """
    Let user pick an image file to use as background.
    When selected, disable video mode.
    """
    global bg_image, use_video_bg
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if path:
        img = cv2.imread(path)
        if img is not None:
            bg_image = img
            use_video_bg = False

def select_video_bg():
    """
    Let user pick a video file to use as background.
    Creates a new VideoCapture object for the selected file.
    """
    global video_cap, use_video_bg
    path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if path:
        # Close any previously open video
        if video_cap:
            video_cap.release()
        video_cap = cv2.VideoCapture(path)
        use_video_bg = True

def toggle_blur():
    """
    Toggle between blur mode and normal background replacement.
    """
    global blur_background
    blur_background = not blur_background

def save_snapshot():
    """
    Save the current processed frame (with background) as an image file.
    Filename includes timestamp to avoid overwriting.
    """
    global last_output_frame
    if last_output_frame is not None:
        filename = f"snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, last_output_frame)
        print(f"Snapshot saved as {filename}")

def update_frame():
    """
    Capture webcam frame, process it with background replacement or blur,
    and update the Tkinter window with the processed image.
    """
    global bg_image, video_cap, last_output_frame

    # Read a frame from webcam
    ret, frame = cap.read()
    if not ret:
        return
    frame = cv2.flip(frame, 1)  # Flip horizontally for mirror effect

    # -------------------------
    # BACKGROUND PREPARATION
    # -------------------------
    if blur_background:
        # Create blurred background directly from webcam frame
        bg_resized = cv2.GaussianBlur(frame, (55, 55), 0)
    else:
        if use_video_bg and video_cap:
            # Read next frame from video background
            ret_bg, bg_frame = video_cap.read()
            if not ret_bg:
                # Restart video when it ends
                video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret_bg, bg_frame = video_cap.read()
            # Resize background video to match webcam resolution
            bg_resized = cv2.resize(bg_frame, (frame.shape[1], frame.shape[0])) if ret_bg else np.zeros_like(frame)
        else:
            # Use static background image
            bg_resized = cv2.resize(bg_image, (frame.shape[1], frame.shape[0])) if bg_image is not None else np.zeros_like(frame)

    # -------------------------
    # SEGMENTATION PROCESS
    # -------------------------
    # Convert BGR to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get segmentation mask (person vs background)
    results = segment.process(rgb_frame)
    mask = results.segmentation_mask
    # Softer edges 
    # Keep mask as float in [0,1]
    alpha = np.clip(mask, 0.0, 1.0)[...,None]
    # feather edges a bit
    alpha = cv2.GaussianBlur(alpha,(9,9),0)
    # Repeat mask into 3 channel 
    alpha = np.repeat(alpha[:,:, None], 3, axis=2)
    output_frame = (alpha * frame + (1 - alpha) * bg_resized).astype(np.uint8) # Blend person & background
    # Store this processed frame for saving snapshots later
    last_output_frame = output_frame.copy()

    # -------------------------
    # DISPLAY IN TKINTER
    # -------------------------
    img = Image.fromarray(cv2.cvtColor(output_frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    lbl_video.imgtk = imgtk  # Keep reference to avoid garbage collection
    lbl_video.configure(image=imgtk)

    # Schedule next frame update
    root.after(10, update_frame)


# -------------------------
# GUI SETUP
# -------------------------

root = tk.Tk()
root.title("Smart Background Replacer")

# Set background color for dark mode style
root.configure(bg="#2C2F33")

# Video display label
lbl_video = tk.Label(root, bg="#2C2F33")
lbl_video.pack(padx=10, pady=10)

# Helper function to create styled buttons
def make_button(text, command, color="#7289DA"):
    """
    Create a styled Tkinter button with given label, function, and color.
    """
    return tk.Button(
        root, text=text, command=command,
        font=("Arial", 12, "bold"), fg="white", bg=color,
        relief="flat", padx=15, pady=8, activebackground="#99AAB5"
    )

# Create and place buttons
make_button("Select Image Background", select_image_bg, "#1ABC9C").pack(pady=5)
make_button("Select Video Background", select_video_bg, "#E67E22").pack(pady=5)
make_button("Toggle Blur", toggle_blur, "#9B59B6").pack(pady=5)
make_button("Save Snapshot", save_snapshot, "#F1C40F").pack(pady=5)
make_button("Quit", root.destroy, "#E74C3C").pack(pady=5)

# Start video update loop
update_frame()

# Start Tkinter main loop
root.mainloop()

# -------------------------
# CLEANUP
# -------------------------
cap.release()
if video_cap:
    video_cap.release()
