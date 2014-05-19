#!/bin/bash

# CKAN dependencies
sudo apt-get update -q
sudo apt-get install solr-jetty
pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.2#egg=ckan'
pip install --allow-all-external -r ~/virtualenv/python2.7/src/ckan/requirements.txt

# ckanext-realtime
python setup.py develop

# Configure Solr
echo -e "NO_START=0\nJETTY_HOST=127.0.0.1\nJETTY_PORT=8983\nJAVA_HOME=$JAVA_HOME" | sudo tee /etc/default/jetty
sudo cp ~/virtualenv/python2.7/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
sudo service jetty restart

# Setup postgres' users and databases
sudo -u postgres psql -c "CREATE USER ckan_default WITH PASSWORD 'pass';"
sudo -u postgres psql -c "CREATE USER datastore_default WITH PASSWORD 'pass';"
sudo -u postgres psql -c 'CREATE DATABASE ckan_default WITH OWNER ckan_default;'
sudo -u postgres psql -c 'CREATE DATABASE datastore_default WITH OWNER ckan_default;'

mkdir links
PROJECT_DIR="`pwd`"
CKAN_DIR="`python -c'import ckan; print ckan.__file__.rsplit("/",2)[0]'`"
cd "$CKAN_DIR"
paster make-config ckan development.ini --no-interactive

sed -i -e 's/^sqlalchemy.url.*/sqlalchemy.url = postgresql:\/\/ckan_default:pass@localhost\/ckan_default/' development.ini
sed -i -e 's/.*datastore.write_url.*/ckan.datastore.write_url = postgresql:\/\/ckan_default:pass@localhost\/datastore_default/' development.ini
sed -i -e '/\[app:main\]/a ckan.realtime.redis_host = 127.0.0.1\nckan.realtime.redis_port = 6379\nckan.realtime.wss_port = 9000' development.ini

sed -i -e 's/^sqlalchemy.url.*/sqlalchemy.url = postgresql:\/\/ckan_default:pass@localhost\/ckan_default/' test-core.ini
sed -i -e 's/.*datastore.write_url.*/ckan.datastore.write_url = postgresql:\/\/ckan_default:pass@localhost\/datastore_default/' test-core.ini
sed -i -e '/\[app:main\]/a ckan.realtime.redis_host = 127.0.0.1\nckan.realtime.redis_port = 6379\nckan.realtime.wss_port = 9000' test-core.ini
sed -i -e 's/.*datastore.read_url.*/ckan.datastore.read_url = postgresql:\/\/datastore_default@\/datastore_default/' test-core.ini

ln -s "$CKAN_DIR"/test-core.ini "$PROJECT_DIR"/links/test-core.ini
ln -s "$CKAN_DIR"/development.ini "$PROJECT_DIR"/links/development.ini
ln -s "$CKAN_DIR"/who.ini "$PROJECT_DIR"/links/who.ini

cat "$PROJECT_DIR"/links/test-core.ini

paster db init -c "$PROJECT_DIR"/links/test-core.ini
paster datastore set-permissions postgres -c "$PROJECT_DIR"/links/test-core.ini

# install jasmine
gem install jasmine

# install dependencies
cd "$PROJECT_DIR"
pip install -r requirements.txt

# start WebSocket server in test mode
cd "$PROJECT_DIR"/bin
python ckan_wss "$PROJECT_DIR"/links/development.ini --test &
