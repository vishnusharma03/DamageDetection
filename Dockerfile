# Build an image that can do training and inference in SageMaker
# This is a Python 3 image that uses the nginx, gunicorn, flask stack
# for serving inferences in a stable way.

#FROM ubuntu:22.04
FROM ubuntu:24.04

# MAINTAINER Amazon AI <sage-learner@amazon.com>

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         libgl1-mesa-dev \
         python3-pip \
         python3-setuptools \
         nginx \
         ca-certificates \
         libglib2.0-0 \
         build-essential \
         zlib1g-dev \
         libffi-dev \
         libssl-dev \
         libbz2-dev \
         liblzma-dev \
         htop \
         nano \
         curl \
    && rm -rf /var/lib/apt/lists/*

# Download and install Python 3.12.2
# RUN wget https://www.python.org/ftp/python/3.12.2/Python-3.12.2.tgz && \
#     tar xvf Python-3.12.2.tgz && \
#     cd Python-3.12.2 && \
#     ./configure && \
#     make && \
#     make install && \
#     cd .. && \
#     rm -rf Python-3.12.2* && \
#     ln -s /usr/local/bin/python3.12 /usr/local/bin/python && \
#     ln -s /usr/local/bin/pip3 /usr/local/bin/pip

RUN wget https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tgz && \
    tar xvf Python-3.11.7.tgz && \
    cd Python-3.11.7 && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf Python-3.11.7* && \
    ln -s /usr/local/bin/python3.11 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3.11 /usr/local/bin/pip


# Install required Python packages
RUN pip --no-cache-dir install opencv-python==4.9.0.80 ultralytics flask gunicorn torch torchvision numpy
# RUN mkdir /datasets
# Set environment variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Copy the program files into the image
COPY container /opt/program
COPY opt/ml /opt/ml

WORKDIR /opt/program

ENTRYPOINT ["train"]

# Optional default command (can be overridden at runtime)
CMD ["train"]

HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:80/ping || exit 1