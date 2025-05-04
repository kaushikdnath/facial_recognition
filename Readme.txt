#docker build -t face_recognition .

docker pull kaushikdnath/face_recognition:1.0

docker run --rm --name face_recog_container -it -v %cd%:/app --add-host=host.docker.internal:host-gateway kaushikdnath/face_recognition:1.0

-v %cmd%:/app(${pwd}:/app for linux) — mount current folder to /app inside the container
-it — interactive terminal
--rm — auto-remove container on exit
--add-host=host.docker.internal:host-gateway --container resolve to the host machine's IP, so your app can connect to DB