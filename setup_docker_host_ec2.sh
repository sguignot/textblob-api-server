#!/bin/sh
# You should use an AMI with docker >= 0.6.1 installed
#
# User data to set in your EC2 instances:
# #!/bin/sh
# set -x -e
# curl https://raw.github.com/sguignot/textblob-api-server/master/setup_docker_host_ec2.sh | sh

set -x -e

echo "Downloading the textblob-api-server docker image..."
docker pull sguignot/textblob-api-server

echo "Install nginx..."
apt-get -qq update
apt-get -qq install nginx

echo "Creating /etc/init/textblob-api-server.conf..."
cat >/etc/init/textblob-api-server.conf <<EOF
description "TextBlob API Server inside Docker"
start on started docker
exec su -l ubuntu -c "docker run -d -p :5000 sguignot/textblob-api-server"
EOF

echo "Creating /etc/nginx/sites-available/default..."
cat >/etc/nginx/sites-available/default <<EOF
upstream http_backend {
  server 127.0.0.1:5000;
  keepalive 16;
}

server {
  listen 80;
  location / {
    proxy_pass http://http_backend;
  }
}
EOF
echo "Restarting nginx..."
service nginx restart

echo "Done."
echo
