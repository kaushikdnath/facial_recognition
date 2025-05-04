import face_recognition
import os
import pickle
from pathlib import Path
import cv2

image_folder="storage/images"
features_file="storage/face_encodings.pkl"
    
def preprocess_image(image_path, max_width=800):
    image = cv2.imread(image_path)
    if image.shape[1] > max_width:
        ratio = max_width / image.shape[1]
        image = cv2.resize(image, (max_width, int(image.shape[0] * ratio)))
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


# Extract facial features
print(f"Extracting facial features")
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
with open(features_file, "wb") as f:
    pickle.dump(encodings_dict, f)
print(f"Saved encodings to: {features_file}")

