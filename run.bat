cmd /k docker run --rm ^
    --name face_recog_container -it ^
    -v %cd%:/app ^
    --add-host=host.docker.internal:host-gateway ^
    kaushikdnath/face_recognition:1.0