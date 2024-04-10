#!/bin/bash

# Update and install necessary packages
sudo yum update -y
sudo yum install -y git nginx
sudo dnf install -y httpd

# Install NVM and Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install 16.0.0

# Clone the repository and build the project
git clone https://github.com/tina35917/rocketweb.git
cd rocketweb
npm install
npm run build

# Move the built files to the web server directory
cd build
sudo mv * /var/www/html
cd
cd /etc/nginx/

# Rewrite nginx.conf file with predefined configuration
cat << EOF | sudo tee tmpnginx.conf > /dev/null

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log notice;
pid /run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                      '\$status \$body_bytes_sent "\$http_referer" '
                      '"\$http_user_agent" "\$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80;
        listen       [::]:80;
        server_name  _;
        root         /var/www/html;

        location / {
            try_files \$uri /index.html;
        }
        location /static/ {
            alias /var/www/html/static/;
        }
        location /media/ {
            # Path to your media files (if applicable)
            alias /var/www/html/media/;
        }
        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
    }
}
EOF

# Overwrite nginx.conf with the predefined configuration
sudo mv tmpnginx.conf nginx.conf

# Start nginx service
sudo systemctl start nginx