# Use the official CUDA image from NVIDIA as a parent image
FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.9 \
    python3.9-distutils \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9 \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.9 as the default python3 and pip3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 \
    && update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3 1

# Install any Python dependencies required by your script
# Assuming you have a requirements.txt file with your Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
ENV BOT_TOKEN ""
ENV LANG "RO"

# Copy your script into the container
COPY . /app

# Set the working directory
WORKDIR /app

# CMD is the default command to run when the container starts
CMD ["python3", "-m", "app"]
