import face_recognition
import shelve
import sys

features_db = "storage/face_encodings.db"

if len(sys.argv) == 1:
    print("Please provide a search image as a parameter.")
    sys.exit(1)

# Load the new image to compare
new_image = face_recognition.load_image_file(sys.argv[1])
new_encodings = face_recognition.face_encodings(new_image)

if not new_encodings:
    print("No face found in the search image.")
    sys.exit(1)

new_encoding = new_encodings[0]

# Open the shelve database
with shelve.open(features_db) as db:
    match_found = False
    for name in db:
        known_encoding = db[name]
        results = face_recognition.compare_faces([known_encoding], new_encoding)
        if results[0]:
            print(f"Match found: {name}")
            match_found = True
            

    if not match_found:
        print("No match found.")
