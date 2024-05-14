# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /Pytuber

# Copy the current directory contents into the container at /Pytuber
COPY . /Pytuber

RUN apt-get update \
    && apt-get install -qq -y build-essential xvfb xdg-utils wget ffmpeg libpq-dev vim libmagick++-dev fonts-liberation sox bc --no-install-recommends\
    && apt-get clean

## ImageMagicK Installation ##
RUN mkdir -p /tmp/distr && \
    cd /tmp/distr && \
    wget https://download.imagemagick.org/ImageMagick/download/releases/ImageMagick-7.1.1-32.tar.xz && \
    tar xvf ImageMagick-7.1.1-32.tar.xz && \
    cd ImageMagick-7.1.1-32 && \
    ./configure --enable-shared=yes --disable-static --without-perl && \
    make && \
    make install && \
    ldconfig /usr/local/lib && \
    cd /tmp && \
    rm -rf distr

## Installing External Font ##
RUN mkdir -p /usr/share/fonts/truetype/custom \
    && for fontname in \
    'Impact'; \
    do \
    modified_fontname=$fontname//[ ]/_}; \
    wget "https://dl.dafont.com/dl/?f=impact" -O $modified_fontname.zip; \
    mkdir -p /usr/share/fonts/truetype/custom; \
    unzip $modified_fontname.zip -d /usr/share/fonts/truetype/custom; \
    rm $modified_fontname.zip; \
    done

# Update font cache
RUN fc-cache -f -v

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# modify ImageMagick policy file so that Textclips work correctly.
#RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml 

# Run cloud_run_main.py when the container launches
CMD ["python", "cloud_run_main.py"]
