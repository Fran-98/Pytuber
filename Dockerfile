# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /Pytuber

# Copy the current directory contents into the container at /app
COPY . /Pytuber

RUN apt update && apt upgrade
RUN apt install libpng-dev libjpeg-dev libtiff-dev
RUN apt install imagemagick


# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "cloud_run_main.py"]