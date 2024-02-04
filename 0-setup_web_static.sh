#!/usr/bin/env bash
# script that sets up my web servers for the deployment of web_static

# install & start NGinx
apt-get -y update
apt-get install -y nginx
service nginx start

# create folders if they don't exist
mkdir /data/web_static/releases/test/
mkdir /data/web_static/shared/
echo "Holberton School" > /data/web_static/releases/test/index.html

# create symbolic link btwn /data/web_static/current & /data/web_static/releases/test/
src_folder="/data/web_static/releases/test/"
dest_folder="/data/web_static/current"
# creates new symbolic link
ln -sf "$src_folder" "$dest_folder"

# giving ownership of /data/ folder to user/group "ubuntu"
chown -R ubuntu:ubuntu /data/

# update Nginx conf file to serve content of /data/web_static/current/ to hbnb_static
location_block="location /hbnb_static/ {\n\talias /data/web_static/current/;\n\tautoindex off;\n}\n"
# Add the location block to the NGinx configuration file
sed -i "/^\s*server\s*{/a $location_block" /etc/nginx/sites-available/default

# restart Nginx to apply conf changes
service nginx restart

# ensure my script/program always exits successfully
exit 0