#!/usr/bin/env bash
#setting up the server

# Check if Nginx is installed; if not, update package list and install Nginx.
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt install nginx -y
fi

# Create the directory /data/ if it does not already exist.
if ! [ -d "/data/" ]; then
    mkdir "/data/"
fi

# Create the /data/web_static/ directory if it does not already exist.
if ! [ -d "/data/web_static/" ]; then
    mkdir "/data/web_static/"
fi

# Create the /data/web_static/releases/ directory if it does not already exist.
if ! [ -d "/data/web_static/releases/" ]; then
    mkdir "/data/web_static/releases/"
fi

# Create the /data/web_static/shared/ directory if it does not already exist.
if ! [ -d "/data/web_static/shared/" ]; then
    mkdir "/data/web_static/shared/"
fi

# Create the /data/web_static/releases/test/ directory if it does not already exist.
if ! [ -d "/data/web_static/releases/test/" ]; then
    mkdir "/data/web_static/releases/test/"
fi

# Create a simple HTML file at /data/web_static/releases/test/index.html for testing Nginx configuration.
touch /data/web_static/releases/test/index.html

PATH_FILE=/data/web_static/releases/test/index.html

content="<html>
<head>
</head>
<body>
	<h1>Testing Nginx configuration</h1>
</body>
</html>"

# Write content to the HTML file.
echo "$content" | sudo tee "$PATH_FILE"

# Create or update a symbolic link /data/web_static/current to point to /data/web_static/releases/test/.
ln -sfn /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ directory and its contents to the ubuntu user and group.
chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve content from /data/web_static/current/ to /hbnb_static.
# Add a location configuration to Nginx.
CONF_PATH=/etc/nginx/nginx.conf
sudo sed -i "/listen 80 default_server;/a\\\tlocation /hbnb_static/ 
{\n\talias /data/web_static/current/;\n\t}" "$CONF_PATH"

# Restart Nginx to apply the changes.
sudo service nginx restart

#!/usr/bin/env bash

# Checking if nginx is installed and installing it if not
# if [ ! -x "$(command -v nginx)" ]; then
#     echo "nginx is not installed, and I will install it now"
#     sudo apt update
#     sudo apt install nginx -y
#     echo "Installation done"
# else
#     echo "nginx is already installed"
# fi

# Creating the required files and setting permissions
# folders=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")
# for folder in "${folders[@]}"; do
#     if [ ! -d "$folder" ]; then
#         echo "Creating $folder"
#         sudo mkdir -p $folder
#         sudo chown -R ubuntu:ubuntu $folder
#     else
#         echo "$folder already exists."
#     fi
# done

# Create index.html inside /data/web_static/releases/test/
# index_file="/data/web_static/releases/test/index.html"
# if [ ! -f "$index_file" ]; then
#     echo "Creating $index_file"
#     sudo sh -c 'echo "<html><head></head><body>Holberton school</body></html>" > '"$index_file"
#     sudo chown ubuntu:ubuntu $index_file
#     echo "Index file created"
# else
#     echo "$index_file already exists."
# fi

# Create symbolic link
# current_link="/data/web_static/current"
# if [ -L "$current_link" ]; then
#     echo "Removing old symbolic link"
#     sudo rm $current_link
# fi
# echo "Creating new symbolic link"
# sudo ln -sf /data/web_static/releases/test/ $current_link

# Permissions
# echo "Setting ownership and permissions"
# sudo chown -R ubuntu:ubuntu /data/

# Nginx Configuration
# nginx_config="/etc/nginx/sites-available/default"
# if [ -f "$nginx_config" ]; then
#     echo "Updating Nginx configuration"
#     sudo sed -i '/^server {/a location /hbnb_static {\n    alias /data/web_static/current;\n}\n' $nginx_config
#     echo "Nginx configuration updated"
    
#     # Testing Nginx configuration
#     sudo nginx -t
    
#     # Restart Nginx
#     echo "Restarting Nginx"
#     sudo service nginx restart
#     echo "Nginx restarted"
# else
#     echo "Nginx configuration file not found"
# fi
