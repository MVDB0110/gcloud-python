#!/bin/bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

sudo apt update
sudo apt -y upgrade
sudo apt-get install -y mongodb-org

sudo cat <<CONF > /etc/mongos.conf
net:
  port: 27017
  bindIpAll: true 
sharding:
  configDB: "ConfigSet/10.0.2.10:27017,10.0.2.11:27017,10.0.2.12:27017"
CONF

mongo 10.0.2.10:27019 --eval 'rs.initiate( { _id: "ConfigSet", configsvr: true, members: [ { _id: 0, host: "10.0.2.10:27019" }, { _id: 1, host: "10.0.2.11:27019" }, { _id: 2, host: "10.0.2.12:27019" } ] } )' > /install

sudo cat <<SYSTEMD > /lib/systemd/system/mongos.service
[Unit]
Description=Mongos systemd file
After=syslog.target
After=network.target

[Service]
User=mongodb
Group=mongodb
Type=forking
RuntimeDirectory=mongodb
RuntimeDirectoryMode=755
PIDFile=/var/run/mongodb/mongos.pid
ExecStart=/usr/bin/mongos --quiet \
    --config /etc/mongos.conf \
    --pidfilepath /var/run/mongodb/mongos.pid \
    --fork
LimitFSIZE=infinity
LimitCPU=infinity
LimitAS=infinity
LimitNOFILE=64000
LimitNPROC=64000

[Install]
WantedBy=multi-user.target
SYSTEMD

sudo systemctl enable --now mongos
sudo echo "\nSucces" >> /install