import face_recognition
import cv2

try:

    # Load the image
    image = face_recognition.load_image_file("storage/image.jpg")

    # Find all face locations
    face_locations = face_recognition.face_locations(image,model='hog')

    # Get the encodings (unique face features)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    # Draw boxes around faces (optional)
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    for top, right, bottom, left in face_locations:
        cv2.rectangle(image_bgr, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the image
    # cv2.imshow("Faces", image_bgr)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Save the result to a file
    cv2.imwrite("storage/output.jpg", image_bgr)

    print(f"Detected {len(face_locations)} face(s). Output saved to output.jpg.")

except Exception as e:
    print(f"An error occurred: {e}")
