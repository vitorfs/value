#!/bin/bash

sudo apt-get update
sudo apt-get -y upgrade

sudo apt-get -y install pwgen
sudo apt-get -y install postgresql postgresql-contrib
sudo apt-get -y install libpq-dev python-dev
sudo apt-get -y install supervisor
sudo apt-get -y install nginx
sudo apt-get -y install python-virtualenv

IP_ADDRESS="$(curl ipecho.net/plain)"
DATABASE_PASSWORD="$(pwgen 32 1)"

su postgres -c "createuser u_value"
su postgres -c "psql -c \"ALTER USER u_value WITH PASSWORD '${DATABASE_PASSWORD}';\"" --preserve-environment
su postgres -c "createdb --owner u_value value"

sudo groupadd --system webapps
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/value_tool value

sudo mkdir -p /webapps/value_tool/
sudo chown value /webapps/value_tool/

su value -c "virtualenv /webapps/value_tool/"
su value -c "source /webapps/value_tool/bin/activate"

cp -r value/ /webapps/value_tool/value

cp /webapps/value_tool/value/conf/gunicorn_start.bash /webapps/value_tool/bin/gunicorn_start

sudo chown -R value:users /webapps/value_tool
sudo chmod -R g+w /webapps/value_tool

su value -c "pip install -r /webapps/value_tool/value/requirements_prod.txt"

SECRET_KEY="$(python /webapps/value_tool/value/scripts/generate_secret_key.py)"

cp /webapps/value_tool/value/conf/app_env /webapps/value_tool/value/.env
sed -i -e 's@{SECRET_KEY}@${SECRET_KEY}@g' /webapps/value_tool/value/.env
sed -i -e 's@{IP_ADDRESS}@${IP_ADDRESS}@g' /webapps/value_tool/value/.env
sed -i -e 's@{DATABASE_PASSWORD}@${DATABASE_PASSWORD}@g' /webapps/value_tool/value/.env

su value -c "python /webapps/value_tool/value/manage.py migrate"
su value -c "python /webapps/value_tool/value/manage.py collectstatic --noinput"

su value -c "mkdir -p /webapps/value_tool/media/"

cp /webapps/value_tool/value/conf/value.conf /etc/supervisor/conf.d/value.conf
su value -c "mkdir -p /webapps/value_tool/logs/"
su value -c "touch /webapps/value_tool/logs/gunicorn_supervisor.log"

su value -c "sudo supervisorctl reread"
su value -c "sudo supervisorctl update"
su value -c "sudo supervisorctl status value"

su value -c "sudo service nginx start"
cp /webapps/value_tool/value/conf/value.nginxconf /etc/nginx/sites-available/value
sed -i -e 's@{IP_ADDRESS}@${IP_ADDRESS}@g' /etc/nginx/sites-available/value
sudo ln -s /etc/nginx/sites-available/value /etc/nginx/sites-enabled/value
su value -c "sudo service nginx restart"

exit 0
