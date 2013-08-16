# textblob-api-server
#
# VERSION        0.1
# DOCKER-VERSION 0.5.3

FROM ubuntu:precise
MAINTAINER Sébastien Guignot "sebastien.guignot@gmail.com"

RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python-pip python-dev gcc curl vim git
RUN apt-get clean

RUN cd /srv && git clone https://github.com/sguignot/textblob-api-server.git
RUN cd /srv/textblob-api-server && pip install -r requirements.txt
RUN curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python

EXPOSE 5000
CMD    ["python", "/srv/textblob-api-server/textblob-api-server.py"]