#!/usr/bin/env bash
# Script to configure and ubuntu server to hosts a static website.

PARENT=/data
DIR1=/data/web_static
DIR2=/data/web_static/releases
DIR3=/data/web_static/shared
DIR4=/data/web_static/releases/test
SYMLINK=/data/web_static/current
TESTFILE=/data/web_static/releases/test/index.html
DIRSTATS="created the following directories:\n\
$PARENT\n$DIR1\n$DIR2\n$DIR3\n$DIR4"
SERVER=nginx

if ! $SERVER -v; then
    echo "nginx is being installed"
    if ! (sudo apt-get update ; sudo apt-get install nginx -y); then
        echo "nginx has failed to install."
	exit 1
    else
        echo "nginx has been installed."
    fi
else
    echo "nginx is installed."
fi

mkdir -p $PARENT
if [ -d "$PARENT" ]; then
    mkdir -p $DIR1
    if [ -d "$DIR1" ]; then
        mkdir -p $DIR2
        if [ -d "$DIR2" ]; then
            mkdir -p $DIR3
            if [ -d "$DIR3" ]; then
                mkdir -p $DIR4
                if [ -d "$DIR4" ]; then
                        echo -e "$DIRSTATS"
                else
                    echo "failed to create the directory $DIR4"
                    exit 1
                fi
            else
                echo "failed to create the directory $DIR3"
                exit 1
            fi
        else
            echo "failed to create the directory $DIR2"
	    exit 1
        fi
    else
        echo "failed to create the directory $DIR1"
	exit 1
    fi
else
    echo "failed to create the directory $PARENT"
    exit 1
fi

if [ -e "$TESTFILE" ]; then
    rm $TESTFILE
    if [ "$(touch $TESTFILE)" ]; then
        echo "failed to create $TESTFILE."
    else
        echo "created $TESTFILE."
    fi
else
    if ! touch $TESTFILE; then
        echo "Failed to create $TESTFILE."
    else
        echo "Created $TESTFILE."
    fi
fi

cat << _EOF_ > $TESTFILE
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
_EOF_

# creates a sym link between symlink to dir4

if [ -L "$SYMLINK" ]; then
    rm $SYMLINK
    if ! ln -sf $DIR4 $SYMLINK; then
        echo "failed to create the sym link between $SYMLINK and $DIR4"
    fi
else
    if ! ln -sf $DIR4 $SYMLINK; then
        echo "failed to create the sym link between $SYMLINK and $DIR4"
    fi
fi

# makes the file owner the ubuntu
if ! chown -R ubuntu: $PARENT; then
    echo -e "Failed to make the $USER user owner of the directory and \
files in $PARENT"
fi 

# updates nginx config to return a defined page when the location is hbnb_static
cat << _EOF_ > /etc/nginx/sites-available/default
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name _;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        add_header X-Served-By $HOSTNAME;

        location /redirect_me {
                return 301 https://www.youtube.com/watch?v=QH2-TGU1wu4;
        }

        error_page 404 /custom404error.html;
        location = /custom404error.html {
                root /var/www/html;
                internal;
        }

	location /hbnb_static {
		alias $SYMLINK;
	}
}
_EOF_

sudo service nginx stop
sudo service nginx start
