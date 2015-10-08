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

sudo -u postgres bash << EOF
createuser u_value
psql -c "ALTER USER u_value WITH PASSWORD '${DATABASE_PASSWORD}';"
createdb --owner u_value value
EOF

sudo groupadd --system webapps
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/value_tool value

sudo mkdir -p /webapps/value_tool/
sudo chown value /webapps/value_tool/

sudo -u value bash << EOF
virtualenv /webapps/value_tool/
EOF

cp -r value/ /webapps/value_tool/value

sudo -u value bash << EOF
source /webapps/value_tool/bin/activate
cp /webapps/value_tool/value/conf/gunicorn_start.bash /webapps/value_tool/bin/gunicorn_start
sudo chmod u+x bin/gunicorn_start
sudo chown -R value:users /webapps/value_tool
sudo chmod -R g+w /webapps/value_tool

pip install -r /webapps/value_tool/value/requirements_prod.txt

SECRET_KEY="$(python /webapps/value_tool/value/scripts/generate_secret_key.py)"

cp /webapps/value_tool/value/conf/app_env /webapps/value_tool/value/.env
sed -i -e 's@{SECRET_KEY}@${SECRET_KEY}@g' /webapps/value_tool/value/.env
sed -i -e 's@{IP_ADDRESS}@${IP_ADDRESS}@g' /webapps/value_tool/value/.env
sed -i -e 's@{DATABASE_PASSWORD}@${DATABASE_PASSWORD}@g' /webapps/value_tool/value/.env

python /webapps/value_tool/value/manage.py migrate
python /webapps/value_tool/value/manage.py collectstatic --noinput
mkdir -p /webapps/value_tool/media/

sudo cp /webapps/value_tool/value/conf/value.conf /etc/supervisor/conf.d/value.conf
mkdir -p /webapps/value_tool/logs/
touch /webapps/value_tool/logs/gunicorn_supervisor.log

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status value

sudo service nginx start
sudo cp /webapps/value_tool/value/conf/value.nginxconf /etc/nginx/sites-available/value
sed -i -e 's@{IP_ADDRESS}@${IP_ADDRESS}@g' /etc/nginx/sites-available/value
sudo ln -s /etc/nginx/sites-available/value /etc/nginx/sites-enabled/value
sudo service nginx restart

EOF

exit 0
