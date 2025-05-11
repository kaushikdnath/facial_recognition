# import pyodbc #for MSSQL pip install pyodbc
import psycopg2 #for postgres and pip install psycopg2-binary
import face_recognition
import shelve
import numpy as np
import cv2
import os

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
cursor.itersize = 1
cursor.execute("SELECT id, name, photo FROM Face_Images")

encodings_dict = {}
with shelve.open("storage/face_encodings.db") as db:
    for row in cursor:
        id, name, photo_data = row
        if photo_data is None or name in db:
            continue

        rgb_image = preprocess_image(photo_data)
        if rgb_image is None:
            print(f"Failed to process image for {name} (ID: {id})")
            continue
        file_path = os.path.abspath(f"D:/Multimedia/Pictures/{name}")
        face_locations = face_recognition.face_locations(rgb_image, model='cnn')
        if not face_locations:
            print(f"No face found in image for {name} (ID: {id}) file:///D:/Multimedia/Pictures/{name}")
            continue

        encodings = face_recognition.face_encodings(rgb_image, known_face_locations=face_locations)
        if encodings:
            db[name] = encodings[0]
            print(f"Saved encoding for {name} (ID: {id}) \033]8;;file://{file_path}\033\\Open File\033]8;;\033\\")

print(f"Saved face encodings to face_encodings.pkl")
