### Dockerfile to build modis block.
FROM ubuntu:18.04
ARG libgdal_ver=3.0.2+dfsg-1~bionic2
# Install packages
RUN apt-get update && apt-get install -y software-properties-common curl
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-add-repository ppa:ubuntugis/ubuntugis-unstable
RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt-get update && apt-get install -y python3.7 python3.7-dev build-essential \
git python3-pip libspatialindex-dev libgdal-dev=${libgdal_ver}
RUN curl -sL https://sentry.io/get-cli/ | bash

# Cleanup apt files so that image size is smaller.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ENVs
ENV PYTHONUNBUFFERED 1

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
ARG manifest

ARG aws_access_key
ARG aws_secret_access_key
ARG aws_region
ARG aws_bucket_name
ARG aws_public_bucket_name

ENV AWS_ACCESS_KEY $aws_access_key
ENV AWS_SECRET_ACCESS_KEY $aws_secret_access_key
ENV AWS_REGION $aws_region
ENV AWS_BUCKET_NAME $aws_bucket_name
ENV AWS_PUBLIC_BUCKET_NAME $aws_public_bucket_name

LABEL "up42_manifest"=$manifest
# Working directory setup.
ADD . /block
WORKDIR /block

RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install -r requirements.txt

# Copy the code into the container.
COPY src /block/src

CMD ["python3.7", "/block/src/run.py"]
