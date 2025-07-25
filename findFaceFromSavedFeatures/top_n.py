import face_recognition
import shelve
import sys

features_db = "storage/face_encodings.db"
top_n = 5  # Change this if you want more/fewer matches

if len(sys.argv) == 1:
    print("Please provide a search image as a parameter.")
    sys.exit(1)
if len(sys.argv) == 3:
    top_n=sys.argv[2]

# Load and encode the new image
new_image = face_recognition.load_image_file(sys.argv[1])
new_encodings = face_recognition.face_encodings(new_image)

if not new_encodings:
    print("No face found in the search image.")
    sys.exit(1)

new_encoding = new_encodings[0]

# Compare against all stored encodings
matches = []

with shelve.open(features_db) as db:
    for name in db:
        known_encoding = db[name]
        distance = face_recognition.face_distance([known_encoding], new_encoding)[0]
        matches.append((name, distance))

# Sort by distance (lower = more similar)
matches.sort(key=lambda x: x[1])

print(f"\nTop {top_n} matches:")
for name, dist in matches[:top_n]:
    print(f"distance = {dist:.4f}, {name}")
