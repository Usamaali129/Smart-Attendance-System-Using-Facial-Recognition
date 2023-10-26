import os.path
import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
from PIL import Image, ImageTk


def get_button(window, image_path, command):
    """
    Create and return a button widget with an image.

    Args:
        window (tk.Tk | tk.Frame): The parent window or frame.
        image_path (str): The path to the button image.
        command (callable): The function to be called when the button is clicked.

    Returns:
        tk.Button: The created button widget.
    """
    image = Image.open(image_path)
    image_width, image_height = image.size

    # Define the desired button size
    button_width = 300
    button_height = 300

    # Calculate the new image size while preserving the aspect ratio
    aspect_ratio = image_width / image_height
    if aspect_ratio >= 1:
        new_width = button_width - 2
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = button_height - 2
        new_width = int(new_height * aspect_ratio)

    image = image.resize((new_width, new_height), Image.LANCZOS)

    # Create a button background image with one-pixel gap
    button_bg = Image.new('RGBA', (button_width, button_height), (0, 0, 0, 0))
    button_bg.paste(image, (1, 1))

    button_image = ImageTk.PhotoImage(button_bg)

    button = tk.Button(
        window,
        image=button_image,
        command=command,
        borderwidth=0,
        highlightthickness=0,
    )

    button.image = button_image

    return button


def get_img_label(window):
    """
    Create and return a label widget for displaying images.

    Args:
        window (tk.Tk | tk.Frame): The parent window or frame.

    Returns:
        tk.Label: The created label widget.
    """
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    """
    Create and return a label widget for displaying text.

    Args:
        window (tk.Tk | tk.Frame): The parent window or frame.
        text (str): The text to be displayed.

    Returns:
        tk.Label: The created label widget.
    """
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    """
    Create and return a text entry widget.

    Args:
        window (tk.Tk | tk.Frame): The parent window or frame.

    Returns:
        tk.Text: The created text entry widget.
    """
    inputtxt = tk.Text(window, height=2, width=15, font=("Arial", 32))
    return inputtxt


def msg_box(title, description):
    """
    Display a message box with the given title and description.

    Args:
        title (str): The title of the message box.
        description (str): The description text in the message box.
    """
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    """
    Recognize a face in the given image using a face recognition database.

    Args:
        img (numpy.ndarray): The image containing the face to be recognized.
        db_path (str): The path to the face recognition database.

    Returns:
        str: The name of the recognized person if found in the database, otherwise 'unknown_person'.
    """
    # It is assumed there will be at most 1 face in the image
    face_locations = face_recognition.face_locations(img)
    if len(face_locations) == 0:
        return 'no_persons_found'

    face_encodings_unknown = face_recognition.face_encodings(img, face_locations)[0]

    db_dir = sorted(os.listdir(db_path))

    for j, file_name in enumerate(db_dir):
        path_ = os.path.join(db_path, file_name)

        try:
            known_face_encodings = face_recognition.face_encodings(cv2.imread(path_))
            match = face_recognition.compare_faces(known_face_encodings, face_encodings_unknown)[0]
            if match:
                return file_name[:-4]  # Return the recognized person's name without the file extension
        except Exception as e:
            # Handle exceptions related to reading the embeddings file (e.g., IOError, EOFError, etc.)
            print(f"Error while processing {file_name}: {e}")

    return 'unknown_person'  # No match found in the database, return 'unknown_person'