# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /Pytuber

# Copy the current directory contents into the container at /Pytuber
COPY . /Pytuber

# Update package list and install necessary system dependencies
# Install numpy using system package manager
RUN apt-get -y update && apt-get -y install ffmpeg imagemagick

# Install some special fonts we use in testing, etc..
RUN apt-get -y install fonts-liberation

RUN apt-get install -y locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8 \
    && rm -rf /var/lib/apt/lists/*
RUN convert -version
# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# modify ImageMagick policy file so that Textclips work correctly.
RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml 

# Run cloud_run_main.py when the container launches
CMD ["python", "cloud_run_main.py"]
