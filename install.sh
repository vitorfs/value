#!/bin/bash

sudo apt-get update
sudo apt-get -y upgrade

sudo apt-get -y install pwgen
sudo apt-get -y install postgresql postgresql-contrib
sudo apt-get -y install libpq-dev python-dev
sudo apt-get -y install supervisor
sudo apt-get -y install nginx
sudo apt-get -y install python-virtualenv

LB="********************************************************************************\n"

printf "$LB Getting public IP address $LB"
IP_ADDRESS="$(curl ipecho.net/plain)"

printf "$LB Generating random database password $LB"
DATABASE_PASSWORD="$(pwgen 32 1)"

printf "$LB Creating postgresql database $LB"
su postgres -c "createuser u_value"
su postgres -c "psql -c \"ALTER USER u_value WITH PASSWORD '${DATABASE_PASSWORD}';\""
su postgres -c "createdb --owner u_value value"

printf "$LB Creating application group and user $LB"
sudo groupadd --system webapps
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/value_tool value

printf "$LB Creating VALUE Tool folder $LB"
sudo mkdir -p /webapps/value_tool/

printf "$LB Assigning user value to application folder $LB"
sudo chown value /webapps/value_tool/

printf "$LB Starting virtual env $LB"
virtualenv /webapps/value_tool/

printf "$LB Coping source code to virtual env $LB"
cp -r value/ /webapps/value_tool/value

printf "$LB Starting virtual env $LB"
source /webapps/value_tool/bin/activate

printf "$LB Copying gunicorn initialization script $LB"
cp /webapps/value_tool/value/conf/gunicorn_start.bash /webapps/value_tool/bin/gunicorn_start

printf "$LB Add execute bit to gunicorn_start $LB"
sudo chmod u+x /webapps/value_tool/bin/gunicorn_start

printf "$LB Installing project dependencies $LB"
pip install -r /webapps/value_tool/value/requirements_prod.txt

printf "$LB Generating application secret key $LB"
SECRET_KEY="$(python /webapps/value_tool/value/scripts/generate_secret_key.py)"

printf "$LB Creating application env file $LB"
cp /webapps/value_tool/value/conf/app_env /webapps/value_tool/value/.env

printf "$LB Add instance specific secret key, ip address, database password $LB"
sed -i "s/{SECRET_KEY}/$SECRET_KEY/" /webapps/value_tool/value/.env
sed -i "s/{IP_ADDRESS}/$IP_ADDRESS/" /webapps/value_tool/value/.env
sed -i "s/{DATABASE_PASSWORD}/$DATABASE_PASSWORD/" /webapps/value_tool/value/.env

printf "$LB Generate application database $LB"
python /webapps/value_tool/value/manage.py migrate

printf "$LB Collect static files $LB"
python /webapps/value_tool/value/manage.py collectstatic --noinput

printf "$LB Creating media folder $LB"
mkdir -p /webapps/value_tool/media/

printf "$LB Copying supervisor script $LB"
sudo cp /webapps/value_tool/value/conf/value.conf /etc/supervisor/conf.d/value.conf

printf "$LB Creating application log folder $LB"
mkdir -p /webapps/value_tool/logs/
touch /webapps/value_tool/logs/gunicorn_supervisor.log

printf "$LB Change application folder rights to value user $LB"
sudo chown -R value:users /webapps/value_tool
sudo chmod -R g+w /webapps/value_tool

printf "$LB Hook application to supervisor $LB"
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status value

printf "$LB Starting NGINX $LB"
sudo service nginx start

printf "$LB Copying configuration files $LB"
sudo cp /webapps/value_tool/value/conf/value.nginxconf /etc/nginx/sites-available/value

printf "$LB Update IP address $LB"
sed -i "s/{IP_ADDRESS}/${IP_ADDRESS}/" /etc/nginx/sites-available/value

printf "$LB Enable site $LB"
sudo ln -s /etc/nginx/sites-available/value /etc/nginx/sites-enabled/value

printf "$LB Restarting NGINX $LB"
sudo service nginx restart

printf "$LB SUCCESS! $LB"

exit 0
