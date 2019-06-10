FROM ubuntu:18.04

RUN mkdir -p /tmp/home
ENV HOME /tmp/home

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git build-essential clang-6.0 lldb-6.0 cmake \
    && apt-get install -y vim wget

RUN apt-get install -y python3-pip

# grader-downloader specific
RUN pip3 install htmlmin

# docker commands
# docker build -t grader-downloader . 
# docker run --rm --mount type=bind,src=$(pwd),target=/temp/home/grader -w /temp/home/grader -it grader-downloader /bin/bash