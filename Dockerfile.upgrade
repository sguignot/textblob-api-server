# textblob-api-server
#
# VERSION        0.1
# DOCKER-VERSION 0.5.3

FROM sguignot/textblob-api-server
RUN cd /srv/textblob-api-server && git pull

EXPOSE 5000
CMD    ["python", "/srv/textblob-api-server/textblob-api-server.py"]