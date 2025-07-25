FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev 

# 2. Cleanup: remove unnecessary tools and caches
RUN apt-get purge -y gnupg \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 3. Install Python dependencies
RUN pip install --no-cache-dir \
    face_recognition \
    opencv-python-headless

WORKDIR /app

CMD ["bash"]
