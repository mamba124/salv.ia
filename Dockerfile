# Use the official CUDA image from NVIDIA as a parent image
FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install dependencies
# Make sure to not install recommends and to clean the 
# install to minimize the size of the container as much as possible.
RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.10 && \
    apt-get install --no-install-recommends -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install any Python dependencies required by your script
# Assuming you have a requirements.txt file with your Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
ENV BOT_TOKEN ""
ENV LANG "RO"
ENV HF_HOME=/opt/dlami/nvme/huggingface_cache

# Copy your script into the container
COPY . /app

# Set the working directory
WORKDIR /app

# CMD is the default command to run when the container starts
CMD ["python3", "-m", "app"]
