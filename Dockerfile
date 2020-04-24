FROM ubuntu:latest

RUN mkdir /data

WORKDIR /data

RUN apt update && \
	apt full-upgrade -y && \
	apt install -y git python3-pip

RUN pip3 install git+https://github.com/MyTheValentinus/bc125csv

ENTRYPOINT ["bc125csv"]
