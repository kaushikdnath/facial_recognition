FROM python:3.10-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install face_recognition
RUN pip install face_recognition
RUN pip install opencv-python-headless

# Set working directory
WORKDIR /app

# Copy your app code (optional)
# COPY . /app

CMD ["bash"]