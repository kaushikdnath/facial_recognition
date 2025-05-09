
#To build Dockerfile to create image run "docker build -t face_recognition ."

#To pull docker image for face_recognition run
docker pull kaushikdnath/face_recognition:1.0

## To run the image either execute "run.bat" or for more control execute below command

docker run --rm --name face_recog_container -it -v %cd%:/app --add-host=host.docker.internal:host-gateway kaushikdnath/face_recognition:1.0

-v %cmd%:/app(${pwd}:/app for linux) — mount current folder to /app inside the container
-it — interactive terminal
--rm — auto-remove container on exit
--add-host=host.docker.internal:host-gateway --container resolve to the host machine's IP, so your app can connect to DB



# Generate Facial Features from "storage/images" folder
python generateAndSaveFacialFeatures/FromDisk/index.py

# Search image for match 
python findFaceFromSavedFeatures/index.py "storage/images/6.JPG"

