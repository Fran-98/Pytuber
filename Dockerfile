# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /Pytuber

# Copy the current directory contents into the container at /Pytuber
COPY . /Pytuber

# Update package list and install necessary system dependencies
ENV DEBIAN_FRONTEND=noninteractive

ARG IM_VERSION=7.1.1-31
ARG LIB_HEIF_VERSION=1.17.6
ARG LIB_AOM_VERSION=3.9.0
ARG LIB_WEBP_VERSION=1.4.0
ARG LIBJXL_VERSION=0.10.2

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y git make gcc pkg-config autoconf curl g++ cmake clang-11 \
    # libaom
    yasm \
    # libheif
    libde265-0 libde265-dev libjpeg-turbo8-dev x265 libx265-dev libtool \
    # libwebp
    libsdl1.2-dev libgif-dev \
    # libjxl
    libbrotli-dev \
    # IM
    libpng16-16 libpng-dev libgomp1 ghostscript libxml2-dev libxml2-utils libtiff-dev libfontconfig1-dev libfreetype6-dev fonts-dejavu liblcms2-dev libtcmalloc-minimal4 \
    # Install manually to prevent deleting with -dev packages
    libxext6 libbrotli1 && \
    # Building libjxl
    export CC=clang-11 CXX=clang++-11 && \
    git clone -b v${LIBJXL_VERSION} https://github.com/libjxl/libjxl.git --depth 1 --recursive --shallow-submodules && \
    cd libjxl && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF .. && \
    cmake --build . -- -j$(nproc) && \
    cmake --install . && \
    cd ../../ && \
    rm -rf libjxl && \
    ldconfig /usr/local/lib && \
    # Building libwebp
    git clone -b v${LIB_WEBP_VERSION} --depth 1 https://chromium.googlesource.com/webm/libwebp && \
    cd libwebp && \
    mkdir build && cd build && cmake ../ && make && make install && \
    ldconfig /usr/local/lib && \
    cd ../../ && rm -rf libwebp && \
    # Building libaom
    git clone -b v${LIB_AOM_VERSION} --depth 1 https://aomedia.googlesource.com/aom && \
    mkdir build_aom && \
    cd build_aom && \
    cmake ../aom/ -DENABLE_TESTS=0 -DBUILD_SHARED_LIBS=1 && make && make install && \
    ldconfig /usr/local/lib && \
    cd .. && \
    rm -rf aom && \
    rm -rf build_aom && \
    # Building libheif \
    git clone -b v${LIB_HEIF_VERSION} --depth 1 https://github.com/strukturag/libheif.git && \
    cd libheif/ && mkdir build && cd build && cmake --preset=release .. && make && make install && cd ../../ && \
    ldconfig /usr/local/lib && \
    rm -rf libheif && \
    # Building ImageMagick
    git clone -b ${IM_VERSION} --depth 1 https://github.com/ImageMagick/ImageMagick.git && \
    cd ImageMagick && \
    ./configure --without-magick-plus-plus --disable-docs --disable-static --with-tiff --with-jxl --with-tcmalloc && \
    make && make install && \
    ldconfig /usr/local/lib && \
    apt-get remove --autoremove --purge -y gcc make cmake clang curl g++ yasm git autoconf pkg-config libpng-dev libjpeg-turbo8-dev libde265-dev libx265-dev libxml2-dev libtiff-dev libfontconfig1-dev libfreetype6-dev liblcms2-dev libsdl1.2-dev libgif-dev libbrotli-dev && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /ImageMagick
    
RUN convert -version
# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run cloud_run_main.py when the container launches
CMD ["python", "cloud_run_main.py"]
