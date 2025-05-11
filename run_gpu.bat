cmd /k docker run --rm -it ^
    --name face_recog_gpu_container ^
    --gpus all ^
    -v %cd%:/app ^
    --add-host=host.docker.internal:host-gateway ^
    face_recognition_gpu bash