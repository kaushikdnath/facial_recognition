import face_recognition
import pickle
import sys

features_file="storage/face_encodings.pkl"
if len(sys.argv)==1:
    print(f"Please provide search image as parameter.")
    exit()

with open(features_file, "rb") as f:
    known_encodings = pickle.load(f)

# Compare a new face
new_image = face_recognition.load_image_file(sys.argv[1])
new_encoding = face_recognition.face_encodings(new_image)[0]

for name, encoding in known_encodings.items():
    results = face_recognition.compare_faces([encoding], new_encoding)
    if results[0]:
        print(f"Match found: {name}")