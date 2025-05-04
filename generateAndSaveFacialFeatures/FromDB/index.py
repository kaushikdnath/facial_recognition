# import pyodbc #for MSSQL pip install pyodbc
import psycopg2 #for postgres and pip install psycopg2-binary
import face_recognition
import pickle
import numpy as np
import cv2
import io

features_file="storage/face_encodings.pkl"
###################### For MSSQL ##########################
# conn_str = (
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=YOUR_SERVER;"
#     "DATABASE=YOUR_DATABASE;"
#     "UID=YOUR_USERNAME;"
#     "PWD=YOUR_PASSWORD;"
# )
# conn = pyodbc.connect(conn_str)
###################### For PostgreSQL #####################
conn = psycopg2.connect(
    host="host.docker.internal",
    database="faces",
    user="postgres",
    password="postgres"
)
###########################################################

def preprocess_image(image_bytes, max_width=800):
    try:
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            return None
        # Resize if needed
        h, w = image.shape[:2]
        if w > max_width:
            scale = max_width / w
            image = cv2.resize(image, (max_width, int(h * scale)))

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return rgb_image
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None


cursor = conn.cursor(name='stream_cursor')  # Named cursor = server-side cursor

cursor.execute("SELECT id, name, photo FROM Face_Images")

encodings_dict = {}
print(f"here")
for row in cursor:
    print(f"here")
    id, name, photo_data = row
    if photo_data is None:
        continue

    rgb_image = preprocess_image(photo_data)
    if rgb_image is None:
        print(f"Failed to process image for {name} (ID: {id})")
        continue

    face_locations = face_recognition.face_locations(rgb_image, model='hog')
    if not face_locations:
        print(f"No face found in image for {name} (ID: {id})")
        continue

    print(f"Encoding for {name} (ID: {id})")
    encodings = face_recognition.face_encodings(rgb_image, known_face_locations=face_locations)
    if encodings:
        encodings_dict[name] = encodings[0]
        # Save after each successful encoding
        with open(encodings_file, "wb") as f:
            pickle.dump(encodings_dict, f)
        print(f"Saved encoding for {name} (ID: {id})")

print(f"Saved {len(encodings_dict)} face encodings to face_encodings.pkl")
