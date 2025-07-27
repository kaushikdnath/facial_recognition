## DOCKER SETUP

# To build Dockerfile to create image run "docker build -t face_recognition ."

# To push to docker 
# 1st Tag "docker tag <local-image-name>:<tag> <dockerhub-username>/<repository-name>:<tag>"
# Next 
# To pull docker image for face_recognition run
docker pull kaushikdnath/face_recognition:latest
# or if Nvidia GPU based 
docker pull kaushikdnath/face_recognition:gpu

## To run the image either execute "run.bat" or for more control execute below command

docker run --rm --name face_recog_container -it -v %cd%:/app --add-host=host.docker.internal:host-gateway kaushikdnath/face_recognition:latest

-v %cmd%:/app(${pwd}:/app for linux) — mount current folder to /app inside the container
-it — interactive terminal
--rm — auto-remove container on exit
--add-host=host.docker.internal:host-gateway --container resolve to the host machine's IP, so your app can connect to DB

#########################################

## VENV SETUP
WINDOWS ::: https://www.python.org/downloads/release/python-3100/
		python3.10 -m venv faceenv
LINUX ::: 	sudo add-apt-repository ppa:deadsnakes/ppa
	  	sudo apt update
		sudo apt install python3.10 python3.10-venv python3.10-dev -y

#Rest are common(for windows with wsl)		
python3.10 -m venv faceenv
source faceenv/bin/activate
sudo apt install build-essential cmake libboost-all-dev -y
pip install dlib
pip install face-recognition-models
pip install face-recognition

#########################################

## RUNNING SCRIPTS

#To generate using CPU set model="hog" and model="cnn" for GPU in face_location function
# Generate Facial Features from "storage/images" folder
python generateAndSaveFacialFeatures/FromDisk/index.py

# Generate Facial Features from DB (run install_Db_drivers.sh)
PYTHONUNBUFFERED=1 python generateAndSaveFacialFeatures/FromDB/index.py 2>&1 | tee storage/log.txt

# Search image for match 
python findFaceFromSavedFeatures/index.py "storage/images/6.JPG"

# Search image for top-n match 
python findFaceFromSavedFeatures/top_n.py "storage/images/6.JPG"


