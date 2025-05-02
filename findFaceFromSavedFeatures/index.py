import face_recognition
import pickle

with open("face_encodings.pkl", "rb") as f:
    known_encodings = pickle.load(f)

# Compare a new face
new_image = face_recognition.load_image_file("random.jpg")
new_encoding = face_recognition.face_encodings(new_image)[0]

for name, encoding in known_encodings.items():
    results = face_recognition.compare_faces([encoding], new_encoding)
    if results[0]:
        print(f"Match found: {name}")