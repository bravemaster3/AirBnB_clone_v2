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
nginx_conf="/etc/nginx/sites-available/default"
content_to_insert="\\
\\    location /hbnb_static {\n\talias /data/web_static/current/;\n\tindex index.html index.htm;\n    }\\
\\
\\    error_page 404 \/404.html;"
if ! grep -qF "location /hbnb_static" "$nginx_conf"
then
    sed -i "/error_page 404 \/404.html;/c $content_to_insert" "$nginx_conf"
fi
service nginx start
