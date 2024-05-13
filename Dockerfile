# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /Pytuber

# Copy the current directory contents into the container at /Pytuber
COPY . /Pytuber

# Update package list and install necessary system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run cloud_run_main.py when the container launches
CMD ["python", "cloud_run_main.py"]
