FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    python3-dev \
    python3-pip \
    python3-gdbm \
    git \
    curl && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/davisking/dlib.git /dlib && \
    cd /dlib && \
    mkdir build && cd build && \
    cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1 && \
    cmake --build . && \
    cd .. && \
    python3 setup.py install

# Install Python packages
RUN pip install --upgrade pip && \
    pip install face_recognition opencv-python-headless psycopg2-binary pyodbc
RUN ln -s /usr/bin/python3.10 /usr/bin/python

WORKDIR /app
CMD ["bash"]
