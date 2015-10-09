#!/bin/bash

LB="\n********************************************************************************\n"

printf "\n$LB UPDATING SYSTEM $LB"
sudo apt-get update
sudo apt-get -y upgrade

printf "\n$LB INSTALLING APPLICATION SERVER DEPENDENCIES $LB"
sudo apt-get -y install pwgen
sudo apt-get -y install postgresql postgresql-contrib
sudo apt-get -y install libpq-dev python-dev
sudo apt-get -y install supervisor
sudo apt-get -y install nginx
sudo apt-get -y install python-virtualenv
sudo apt-get -y install libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

printf "\n$LB GETTING PUBLIC IP ADDRESS $LB"
IP_ADDRESS="$(curl ipecho.net/plain)"

printf "\n$LB GENERATING RANDOM DATABASE PASSWORD $LB"
DATABASE_PASSWORD="$(pwgen 32 1)"

printf "\n$LB CREATING POSTGRESQL DATABASE $LB"
su - postgres -c "createuser u_value"
su - postgres -c "psql -c \"ALTER USER u_value WITH PASSWORD '${DATABASE_PASSWORD}';\""
su - postgres -c "createdb --owner u_value value"

printf "\n$LB CREATING APPLICATION GROUP AND USER $LB"
sudo groupadd --system webapps
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/value_tool value

printf "\n$LB CREATING VALUE TOOL FOLDER $LB"
sudo mkdir -p /webapps/value_tool/

printf "\n$LB ASSIGNING USER VALUE TO APPLICATION FOLDER $LB"
sudo chown value /webapps/value_tool/

printf "\n$LB STARTING VIRTUAL ENV $LB"
virtualenv /webapps/value_tool/

printf "\n$LB COPYING SOURCE CODE TO VIRTUAL ENV $LB"
cp -r ../value/ /webapps/value_tool/value

printf "\n$LB STARTING VIRTUAL ENV $LB"
source /webapps/value_tool/bin/activate

printf "\n$LB COPYING GUNICORN INITIALIZATION SCRIPT $LB"
cp /webapps/value_tool/value/conf/gunicorn_start.bash /webapps/value_tool/bin/gunicorn_start

printf "\n$LB ADD EXECUTE BIT TO GUNICORN_START $LB"
sudo chmod u+x /webapps/value_tool/bin/gunicorn_start

printf "\n$LB INSTALLING PROJECT DEPENDENCIES $LB"
pip install -r /webapps/value_tool/value/requirements_prod.txt

printf "\n$LB GENERATING APPLICATION SECRET KEY $LB"
APP_SECRET_KEY="$(python /webapps/value_tool/value/scripts/generate_secret_key.py)"

printf "\n$LB CREATING APPLICATION ENV FILE $LB"
cp /webapps/value_tool/value/conf/app_env /webapps/value_tool/value/.env

printf "\n$LB ADD INSTANCE SPECIFIC SECRET KEY, IP ADDRESS, DATABASE PASSWORD $LB"
sed -i "s/{APP_SECRET_KEY}/$APP_SECRET_KEY/" /webapps/value_tool/value/.env
sed -i "s/{IP_ADDRESS}/$IP_ADDRESS/" /webapps/value_tool/value/.env
sed -i "s/{DATABASE_PASSWORD}/$DATABASE_PASSWORD/" /webapps/value_tool/value/.env

printf "\n$LB GENERATE APPLICATION DATABASE $LB"
python /webapps/value_tool/value/manage.py migrate

printf "\n$LB COLLECT STATIC FILES $LB"
python /webapps/value_tool/value/manage.py collectstatic --noinput

printf "\n$LB CREATING MEDIA FOLDER $LB"
mkdir -p /webapps/value_tool/media/

printf "\n$LB COPYING SUPERVISOR SCRIPT $LB"
sudo cp /webapps/value_tool/value/conf/value.conf /etc/supervisor/conf.d/value.conf

printf "\n$LB CREATING APPLICATION LOG FOLDER $LB"
mkdir -p /webapps/value_tool/logs/
touch /webapps/value_tool/logs/gunicorn_supervisor.log

printf "\n$LB CHANGE APPLICATION FOLDER RIGHTS TO VALUE USER $LB"
sudo chown -R value:users /webapps/value_tool
sudo chmod -R g+w /webapps/value_tool

printf "\n$LB HOOK APPLICATION TO SUPERVISOR $LB"
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status value

printf "\n$LB STARTING NGINX $LB"
sudo service nginx start

printf "\n$LB COPYING CONFIGURATION FILES $LB"
sudo cp /webapps/value_tool/value/conf/value.nginxconf /etc/nginx/sites-available/value

printf "\n$LB UPDATE IP ADDRESS $LB"
sed -i "s/{IP_ADDRESS}/${IP_ADDRESS}/" /etc/nginx/sites-available/value

printf "\n$LB ENABLE SITE $LB"
sudo ln -s /etc/nginx/sites-available/value /etc/nginx/sites-enabled/value

printf "\n$LB RESTARTING NGINX $LB"
sudo service nginx restart

printf "\n$LB CREATE THE ADMIN USER: $LB"
python /webapps/value_tool/value/manage.py createsuperuser

printf "\n$LB SUCCESS! $LB"

exit 0
