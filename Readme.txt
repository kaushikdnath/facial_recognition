#docker build -t face_recognition .

docker pull kaushikdnath/face_recognition:1.0

docker run --rm --name face_recog_container -it -v %cd%:/app face_recognition

-v %cmd%:/app(${pwd}:/app for linux) — mount current folder to /app inside the container
-it — interactive terminal
--rm — auto-remove container on exit
