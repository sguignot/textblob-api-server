# textblob-api-server
#
# VERSION        0.1
# DOCKER-VERSION 0.5.3

FROM ubuntu:precise
MAINTAINER Sébastien Guignot "sebastien.guignot@gmail.com"

RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y curl git python-pip python-dev gcc && apt-get clean
RUN cd /srv && git clone https://github.com/sguignot/textblob-api-server.git
RUN cd /srv/textblob-api-server && pip install -r requirements.txt
RUN /srv/textblob-api-server/install_corpora.sh

EXPOSE 5000
CMD    ["python", "/srv/textblob-api-server/textblob-api-server.py"]