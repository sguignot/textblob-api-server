textblob-api-server
===================

This is just [TextBlob](https://github.com/sloria/TextBlob) + [flask](https://github.com/mitsuhiko/flask) + ajax = *Live sentiment analysis while you're typing*

[Try Demo online](http://textblob-api-1743413701.us-east-1.elb.amazonaws.com) *(docker image running on a EC2 ubuntu instance)*

## Install and run

### From the [docker](http://docker.io) repository:
```bash
docker run sguignot/textblob-api-server
```

##### You can also build a docker image from the Dockerfile:
```bash
docker build https://raw.github.com/sguignot/textblob-api-server/master/Dockerfile
```
