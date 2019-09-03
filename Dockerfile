FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git build-essential clang-6.0 lldb-6.0 cmake \
    && apt-get install -y vim wget

RUN apt-get install -y python3-pip

# grader-downloader specific
RUN pip3 install htmlmin requests

# add a non root user
ARG USER_NAME=grader
ENV USER_NAME=$USER_NAME

RUN adduser $USER_NAME
RUN mkdir -p /etc/sudoers.d
RUN echo "$USER_NAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USER_NAME && \
    chmod 0440 /etc/sudoers.d/$USER_NAME

RUN chmod -R a+rw /home/$USER_NAME/
RUN apt-get install -y sudo
USER $USER_NAME

# docker commands
# docker build -t grader-downloader . 
# docker run --rm --mount type=bind,src=$(pwd),target=/temp/home/grader -w /temp/home/grader -it grader-downloader /bin/bash