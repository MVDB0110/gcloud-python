#!/bin/bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt update
sudo apt -y upgrade
sudo apt-get install -y mongodb-org nano
sudo cat <<MONGO > /etc/mongod.conf
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log
net:
  port: 27019
  bindIpAll: true
processManagement:
  timeZoneInfo: /usr/share/zoneinfo
replication:
  replSetName: "ConfigSet"
sharding:
   clusterRole: configsvr
MONGO
sudo systemctl enable --now mongod
echo "Succes" > /install