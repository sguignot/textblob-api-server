textblob-api-server
===================

This is just [TextBlob](https://github.com/sloria/TextBlob) + [flask](https://github.com/mitsuhiko/flask) + ajax = *Live sentiment analysis while you're typing*

[Try Demo online](http://ec2-54-246-227-90.eu-west-1.compute.amazonaws.com:5000/index.html) *(docker image running on a EC2 ubuntu instance)*

## Install and run

### From the [docker](http://docker.io) repository:
```bash
docker run sguignot/textblob-api-server
```

##### You can also build a docker image from the Dockerfile:
```bash
docker build https://raw.github.com/sguignot/textblob-api-server/master/Dockerfile
```
