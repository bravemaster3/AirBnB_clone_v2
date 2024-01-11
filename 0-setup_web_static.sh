#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static.
# Installation of nginx if not already installed
if ! command -v nginx &> /dev/null
then
    apt-get update
    apt-get install -y nginx
fi
service nginx start

#folder creations
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
ubuntu@89-web-01:~/$ curl localhost/hbnb_static/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | tee /data/web_static/releases/test/index.html > /dev/null 2>&1

# Symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Ownership
chown -hR ubuntu:ubuntu /data/

# creating /hbnb_static location
nginx_conf="/etc/nginx/sites-available/default"
content_to_insert="\\
\\
\\    location /hbnb_static {\\n\\talias /data/web_static/current/;\\n\\tindex index.html index.htm;\\n    }"
if ! grep -qF "location /hbnb_static" "$nginx_conf"
then
    sed -i "/error_page 404 \/404.html;/a $content_to_insert" "$nginx_conf"
fi

service nginx restart
