import face_recognition
import os
import pickle
from pathlib import Path

def extract_and_save_face_encodings(image_folder, output_file):
    encodings_dict = {}

    for image_file in Path(image_folder).glob("*.*"):
        # Load the image
        image = face_recognition.load_image_file(image_file)
        face_encodings = face_recognition.face_encodings(image)

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

# Example usage
extract_and_save_face_encodings("images", "face_encodings.pkl")
