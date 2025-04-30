# Инструкция по развертыванию проекта

## 1. Установка зависимостей

Установите необходимые пакеты:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```
## 2. Клонирование проекта
```
git clone https://github.com/Sosigenus/mdum2025.git
cd mdum2025
```
## 3. Настройка DB PostgreSQL
```
sudo -u postgres psql
```
```
CREATE DATABASE geo_db;
CREATE USER geo_user WITH PASSWORD 'geo_pass';
ALTER ROLE geo_user SET client_encoding TO 'utf8';
ALTER ROLE geo_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE geo_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE geo_db TO geo_user;
\q
```
## 4. Миграции
```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```
## 5. Настройка Gunicorn
Добавим виртуальное окружение:
```
source /home/maxim/venv/bin/activate
```
```
python3 -m venv /home/maxim/venv
source /home/maxim/venv/bin/activate
```
```
pip install django gunicorn
```

Создайте файл /etc/systemd/system/gunicorn.service:
```
[Unit]
Description=gunicorn daemon for geo_project
After=network.target

[Service]
User=maxim
Group=maxim
WorkingDirectory=/home/maxim/PycharmProjects/geo_project
ExecStart=/home/maxim/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8001 geo_project.wsgi:application

[Install]
WantedBy=multi-user.target
```
Перезапуск и активация сервиса:
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```
## 6. Настройка Nginx
Создайте файл /etc/nginx/sites-available/geo_project:
```
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/maxim/PycharmProjects/geo_project/staticfiles;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Cвязываем файлы:
```
sudo ln -s /etc/nginx/sites-available/geo_project /etc/nginx/sites-enabled/
```
Перезапуск nginx:
```
sudo nginx -t
sudo systemctl restart nginx
```
## 7. Готово
Test:
```
http://localhost
```
p.s.
Остановить всё сразу:
```
sudo systemctl stop nginx
sudo systemctl stop gunicorn
```
