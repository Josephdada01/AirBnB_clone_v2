#!/usr/bin/env bash
#writing this script to setup the server for deployment

#The below script install nginx if not already install
if [ ! -x "$(command -v nginx)" ]; then
	echo "nginx is not install, and i will install it now"
	sudo apt update
	sudo apt install nginx -y
	echo "installation done"
else
	echo "nginx is already installed"

fi

#creating the required files if they dont exist
folders=("/data/" "/data/web_static/" "/data/web_static/releases/"
	"/data/web_static/shared/" "data/web_static/releases/test/")
for folder in "${folders[@]}"
do
	if [ ! -d "$folder" ]; then
		echo "creating the files"
		sudo mkdir -p $folder
		sudo chown -R ubuntu:ubuntu $folder
	else
		echo "$folder already exist"

	fi
done

#creating index.html in data/web_static/releases/test/index.html with content
the_index="/data/web_static/releases/test/index.html"
if [ ! -f "$the_index" ]; then
	echo "will create the $the_index now"
	sudo sh -c 'echo "<html><head></head><body>Holberton School
	</body></html>" > ' "$the_index"
	sudo chown ubuntu:ubuntu $the_index
	echo "the index create successfully"
else
	echo "$the_index already exists"
fi

#creating symbolic link
current_link="/data/web_static/current"
if [ -L "$current_link" ]; then
	echo "Removing old symbolic link..."
	sudo rm $current_link
fi
echo "creating new symbolic link"
sudo ln -s /data/web_static/releases/test $current_link

#updating the nginx configuration
nginx_config="/etc/nginx/sites-available/default"

if [ -f "$nginx_config" ]; then
	sudo sed -i "/^server {/a location /hbnb_static {\n 
	alias /data/web_static/current/;\n}\n" $nginx_config
	echo "nginx configuration done"
else
	echo "configuration not found"

fi

nginx -t

sudo service nginx restart
