#!/usr/bin/env bash

# Install Nginx if not installed
if [ ! -x "$(command -v nginx)" ]; then
    echo "nginx is not installed, and I will install it now"
    sudo apt update
    sudo apt install nginx -y
    echo "Installation done"
else
    echo "nginx is already installed"
fi

# Creating the required files and setting permissions
folders=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")
for folder in "${folders[@]}"; do
    if [ ! -d "$folder" ]; then
        echo "Creating $folder"
        sudo mkdir -p $folder
        sudo chown -R ubuntu:ubuntu $folder
    else
        echo "$folder already exists."
    fi
done

# Create index.html inside /data/web_static/releases/test/
index_file="/data/web_static/releases/test/index.html"
if [ ! -f "$index_file" ]; then
    echo "Creating $index_file"
    sudo sh -c 'echo "<html><head></head><body>Holberton school</body></html>" > '"$index_file"
    sudo chown ubuntu:ubuntu $index_file
    echo "Index file created"
else
    echo "$index_file already exists."
fi

# Create symbolic link
current_link="/data/web_static/current"
if [ -L "$current_link" ]; then
    echo "Removing old symbolic link"
    sudo rm $current_link
fi
echo "Creating new symbolic link"
sudo ln -sf /data/web_static/releases/test/ $current_link

# Permissions
echo "Setting ownership and permissions"
sudo chown -R ubuntu:ubuntu /data/

# Nginx Configuration
nginx_config="/etc/nginx/sites-available/default"
if [ -f "$nginx_config" ]; then
    echo "Updating Nginx configuration"
    sudo sed -i '/^server {/a location /hbnb_static {\n    alias /data/web_static/current;\n}\n' $nginx_config
    echo "Nginx configuration updated"
    
    # Testing Nginx configuration
    sudo nginx -t
    
    # Restart Nginx
    echo "Restarting Nginx"
    sudo service nginx restart
    echo "Nginx restarted"
else
    echo "Nginx configuration file not found"
fi
