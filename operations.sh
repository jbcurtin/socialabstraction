#!/usr/bin/env bash

set -x
set -e

# Before running this script, you'll want to create an SSH configuration entry in $HOME/.ssh/config with 'psf' as the
# host. Then alter this file to point to a domain you control.
HOST_NAME=psf
HOST_SSH_OPTIONS='-o ConnectTimeout=3'
PSQL_USER='social'
PSQL_PASSWORD='abstraction'
PSQL_DB='socialabstraction'
# Not a production enviornment; I'll worry about secrets in the repo another day
PSQL_DOCKER_CMD="docker run -e POSTGRES_USER=$PSQL_USER -e POSTGRES_PASSWORD=$PSQL_PASSWORD -e POSTGRES_DB=$PSQL_DB -p 5432:5432 -d postgres"
REDIS_DOCKER_CMD="docker run -p 6379:6379 -d redis"

if [ "$1" == 'bootstrap' ]; then
  if ! ssh $HOST_SSH_OPTIONS $HOST_NAME "ls /tmp" 1>/dev/null 2>/dev/null; then
    echo 2>1 'Unable to identify a proxy. Please launch a micro-instance to setup the reverse-proxy'
    echo 2>1 'https://cloud-images.ubuntu.com/locator/ec2/'
    exit 1
  fi
  if [ ! -d "env-service" ]; then
    virtualenv -p $(which python3) env-service
  fi
  source env-service/bin/activate
  # pip install -r requirements.txt
  $PSQL_DOCKER_CMD 2>/dev/null || true
  # Make sure to alter $HOST_NAME.jbcurtin.io to a DNS record of your choosing
  cat > /tmp/Caddyfile <<EOF
$HOST_NAME.jbcurtin.io {
  tls $HOST_NAME-proxy@jbcurtin.io
  proxy / http://localhost:8000 {
    transparent
    websocket
  }
}
EOF
  ssh $HOST_NAME "curl -sSL https://gist.githubusercontent.com/jbcurtin/ea10d25475de401360fd9d44b5d392ac/raw/c2d185eb08dd3773aa8b87068ef693068e7a50d3/install-docker.sh |sudo sh" || true
  echo "Waiting for service[$HOST_NAME] to come back online"
  while true; do
    if ssh $HOST_SSH_OPTIONS $HOST_NAME "ls /tmp" 1>/dev/null 2>/dev/null; then
      break
    fi
    sleep 1
  done
  echo "Service[$HOST_NAME] back online"
  scp /tmp/Caddyfile $HOST_NAME:
  ssh $HOST_NAME "docker run -v /home/ubuntu/Caddyfile:/etc/Caddyfile:ro -v /home/ubuntu/certs:/root/.caddy:rw -p 80:80 -p 443:443 --network=host -d wemakeservices/caddy-docker:latest"
  if [ -z "$(ps aux |grep "8000:localhost:8000" |grep -v 'grep' |awk '{print $2}')" ];then
    autossh -M 23444 -f -N $HOST_NAME -R 8000:*:8000 -C
  fi;
  echo 'Connect to DB with URL:'
  echo "postgresql://$PSQL_USER:$PSQL_PASSWORD@localhost:5432/$PSQL_DB"
fi

