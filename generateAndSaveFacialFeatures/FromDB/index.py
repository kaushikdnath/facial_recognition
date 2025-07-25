import pyodbc #for MSSQL pip install pyodbc
# import psycopg2 #for postgres and pip install psycopg2-binary
import face_recognition
import shelve
import numpy as np
import cv2

features_file="storage/face_encodings.pkl"
###################### For MSSQL ##########################
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=10.179.46.3;"
    "DATABASE=cctns_state_db;"
    "UID=sa;"
    "PWD=megpol;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
###################### For PostgreSQL #####################
# conn = psycopg2.connect(
#     host="host.docker.internal",
#     database="faces",
#     user="postgres",
#     password="postgres"
# )
# cursor = conn.cursor(name='stream_cursor')  # Named cursor = server-side cursor PostgresSQL
# cursor.itersize = 1                         # PostgresSQL
###########################################################

def preprocess_image(image_bytes, max_width=800):
    try:
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            print("cv2.imdecode returned None")
            return None

        h, w = image.shape[:2]
        if w > max_width:
            scale = max_width / w
            image = cv2.resize(image, (max_width, int(h * scale)))

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return rgb_image,image
    except cv2.error as e:
        print(f"OpenCV error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error preprocessing image: {e}")
        return None

#accused files
sql_accused="SELECT f.accused_srno as id,CAST(f.accused_srno AS VARCHAR(100)) as name, UPLOADED_FILE AS photo " \
    "FROM t_accused_files f " \
    "where f.file_type_cd=1 and f.file_subtype_cd=14 and f.record_status='C' "
#Deadbody
sql_dead="SELECT db_inquest_num as id,CAST(db_inquest_num AS VARCHAR(100)) as name, UPLOADED_FILE AS photo " \
    "FROM t_deadbody_files f " \
    "where f.file_type_cd=1 and file_subtype_cd=14 and f.file_belongs_to='PHOTO_UPLOAD' and f.record_status='C' "


cursor.execute(sql_accused)

encodings_dict = {}
with shelve.open("storage/face_encodings.db") as db:
    # Postgres #############################################################
    # for row in cursor:                              
    # MSSQL ################################################################
    while True:
        row = cursor.fetchone()
        if not row:
            break
        ####################################################################
        id, name, photo_data = row
        if photo_data is None or name in db:
            continue

        rgb_image,image = preprocess_image(photo_data)
        if rgb_image is None:
            print(f"Failed to process image for {name} (ID: {id})")
            continue
        face_locations = face_recognition.face_locations(rgb_image, model='hog')
        if not face_locations:
            print(f"No face found in image for {name} (ID: {id}) ")
            # Save the image using cv2.imwrite
            cv2.imwrite(f"storage/noface/{name}.jpg", image)
            continue

        encodings = face_recognition.face_encodings(rgb_image, known_face_locations=face_locations)
        if encodings:
            db[name] = encodings[0]
            print(f"Saved encoding for {name} (ID: {id})")

print(f"Saved face encodings to face_encodings.pkl")
