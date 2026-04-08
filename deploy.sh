#!/bin/bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx
git clone https://github.com/devgenix/django-link-shortener-app.git /home/ubuntu/app
cd /home/ubuntu/app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
sudo tee /etc/systemd/system/django.service > /dev/null <<EOF
[Unit]
Description=Gunicorn instance to serve Django
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/app
Environment="PATH=/home/ubuntu/app/venv/bin"
ExecStart=/home/ubuntu/app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 core.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl start django
sudo systemctl enable django

sudo tee /etc/nginx/sites-available/django > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
