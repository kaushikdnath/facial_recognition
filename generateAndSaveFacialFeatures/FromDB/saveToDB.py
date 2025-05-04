import os
import psycopg2
import sys

# Database connection parameters
DB_HOST = 'localhost'
DB_NAME = 'faces'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

if len(sys.argv)==1:
    print(f"Please provide search image as parameter.")
    exit()
pathToImages=sys.argv[1]

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Get all image files in current directory
supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
files = [f for f in os.listdir(pathToImages) if f.lower().endswith(supported_extensions)]

# Insert each image
i=65
for filename in files:
    with open(pathToImages+filename, 'rb') as f:
        binary_data = f.read()
        cursor.execute(
            "INSERT INTO face_images (name, photo) VALUES (%s, %s)",
            (filename, psycopg2.Binary(binary_data))
        )
        i+=1
        print(f"Inserted {filename}")

# Commit and close
conn.commit()
cursor.close()
conn.close()
print("All images inserted successfully.")