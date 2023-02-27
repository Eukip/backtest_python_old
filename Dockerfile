FROM ubuntu:latest

WORKDIR /app
RUN rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true
COPY ./src /app

RUN apt-get update

RUN apt update
RUN apt -y upgrade

RUN apt-get -qq -y install software-properties-common
RUN apt-get -qq -y install python3
RUN apt-get -qq -y install -y pip

COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt

