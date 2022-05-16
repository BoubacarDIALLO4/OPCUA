#!/usr/bin/bash env

#bun-level Startup script for curlftpfs
#
# chkconfig: 345 91 19
# description: Startup / Shutdown the curlftpfs

# FTP user, password, and host (you can specify the port also eg. Ftp.example.com:2002)
ftpUser=user
ftpPass=password
ftpHost=127.0.0.1
MOUNTPOINT="/mnt/ftp"

# Mounted to folder
mPath="/opt/mounted/ftp"

# Create the mounted to dir if doesn't exist
if [ ! -d $mPath ]; then
sudo mkdir -p $mPath
fi

if cat /proc/mounts | grep ${MOUNTPOINT} > /dev/null; then
       echo "${MOUNTPOINT} already mounted."
else
       echo "Mounted path"
       curlftpfs $ftpHost $mPath -o user=$ftpUser: $ftpPass, allow_other
fi

