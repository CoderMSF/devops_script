#!/bin/bash
MONGO_PATH=/home/$USER/server/mongodb-4.2.9/bin
CURRENT_DATE=$(date "+%Y-%m-%d")
LAST_DATE=$(date --date='7 day ago' "+%Y-%m-%d")
BACKUP_DIR=/mnt2/mongodb/mongodata-$CURRENT_DATE
LAST_BACKUP_DIR=/mnt2/mongodb/mongodata-$LAST_DATE
HOST_IP=192.168.1.213
HOST_PORT=27017
nohup $MONGO_PATH/mongodump -h $HOST_IP:$HOST_PORT -u root -p root -o $BACKUP_DIR --gzip >> nohup.log &
if [ $? -ne 0 ]; then
    echo "mongodb command execute failed!"
else
    echo "mongodump successed"
    if [ -d $LAST_BACKUP_DIR ]; then
        rm -rf $LAST_BACKUP_DIR
    fi
fi
