import face_recognition
import os
import pickle
from pathlib import Path
import cv2

def preprocess_image(image_path, max_width=800):
    """
    Loads an image, resizes it if too large, and converts it to RGB format.
    
    Args:
        image_path (str): Path to the image file.
        max_width (int): Max width to resize the image for faster processing.

    Returns:
        numpy.ndarray: The preprocessed RGB image.
    """
    # Load the image using OpenCV (BGR format)
    image = cv2.imread(image_path)

    # if image is None:
    #     raise FileNotFoundError(f"Image not found: {image_path}")

    height, width = image.shape[:2]

    # Resize if necessary
    if width > max_width:
        ratio = max_width / width
        image = cv2.resize(image, (max_width, int(height * ratio)))

    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return rgb_image


def extract_and_save_face_encodings(image_folder, output_file):
    encodings_dict = {}

    for image_file in Path(image_folder).glob("*.*"):
        # Load the image
        # image = face_recognition.load_image_file(image_file)
        image = preprocess_image(image_file)
        # face_encodings = face_recognition.face_encodings(image)

        face_locations = face_recognition.face_locations(image, model='hog') #cnn for slower but accurate and "hog" for faster performance
        face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)

        if face_encodings:
            # Take the first face found (you can adapt this for multiple)
            encodings_dict[image_file.name] = face_encodings[0]
            print(f"Encoded: {image_file.name}")
        else:
            print(f"No face found in: {image_file.name}")

    # Save all encodings to a file
    with open(output_file, "wb") as f:
        pickle.dump(encodings_dict, f)
    print(f"Saved encodings to: {output_file}")

# Extract facial features
print(f"Extracting facial features")
extract_and_save_face_encodings("images", "face_encodings.pkl")
