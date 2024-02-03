#!/usr/bin/env bash
# script that sets up my web servers for the deployment of web_static

# install & start NGinx
apt update
apt install -y nginx
systemctl start nginx

# create folders if they don't exist
mkdir /data/web_static/releases/test/
mkdir /data/web_static/shared/
touch /data/web_static/releases/test/index.html
echo "Hi Eljones👋, Am served from Nginx" > /data/web_static/releases/test/index.html

# create symbolic link btwn /data/web_static/current & /data/web_static/releases/test/
src_folder="/data/web_static/releases/test/"
dest_folder="/data/web_static/current"
# check if symbolic already exists & delete it
if [ -L "$dest_folder" ]; then
    rm "$dest_folder"
fi
# creates new symbolic link
sudo ln -s "$src_folder" "$dest_folder"

# giving ownership of /data/ folder to user/group "ubuntu"
sudo chown -R ubuntu:ubuntu /data

# update Nginx conf file to serve content of /data/web_static/current/ to hbnb_static
nginx_conf="/etc/nginx/sites-available/default"
# configure location block in the server context > Mginx.conf file
sudo tee -a "$nginx_conf" > /dev/null <<EOL
server {
    listen 80;
    server_name eljones.tech;

    location /hbnb_static {
        alias /data/web_static/current; # alias specifies dir from which to serve requests to /hbnb_statuc
        index index.html; # default files to serve
    }
}
EOL

# restart Nginx to apply conf changes
sudo systemctl restart nginx

# ensure my script/program always exits successfully
exit 0