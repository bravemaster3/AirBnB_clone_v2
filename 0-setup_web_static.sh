#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static.
# Installation of nginx if not already installed
if ! command -v nginx &> /dev/null
then
    apt-get update
    apt-get upgrade
    apt-get install -y nginx
fi
#folder creations
mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
echo "Hello Again World!" | tee /data/web_static/releases/test/index.html
# Symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current
# Ownership
chown -hR ubuntu:ubuntu /data/
# creating /hbnb_static location
printf '%s%n' "server {
    listen 80;
    listen [::]:80;

    add_header X-Served-By 422381-web-01;

    server_name bravemaster.tech www.bravemaster.tech;
    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm 0-index.html;
    }

    error_page 404 /404.html;

    location /404 {
        root /var/www/html;
        internal;
    }
}" > /etc/nginx/sites-available/default
service nginx start
