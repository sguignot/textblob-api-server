# textblob-api-server
#
# VERSION        0.1
# DOCKER-VERSION 0.5.3

FROM ubuntu:precise
MAINTAINER Sébastien Guignot "sebastien.guignot@gmail.com"

RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update

# First get needed stuff from github (do not waste too much time in case of failure)
RUN apt-get install -y curl git python-nltk
RUN cd /srv && git clone https://github.com/sguignot/textblob-api-server.git
RUN cd /tmp && git clone https://github.com/sloria/TextBlob.git
RUN cd /tmp/TextBlob && git checkout 0.5.2 && python download_corpora.py

# Install python base
RUN apt-get install -y python-pip python-dev gcc vim
# Cleanup downloaded packages
RUN apt-get clean

# Install python deps
RUN cd /srv/textblob-api-server && pip install -r requirements.txt

EXPOSE 5000
CMD    ["python", "/srv/textblob-api-server/textblob-api-server.py"]