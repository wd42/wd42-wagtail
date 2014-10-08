#!/usr/bin/env bash

# Quit when errors happen
set -e

# Helper to run a command as another user
function as () {
	local user="$1"
	shift
	sudo -u "$user" "$@"
}

v_home=~vagrant
p_name="dev42"
p_root="/srv/$p_name"  # Path to the code
p_venv="${v_home}/${p_name}_venv"  # Where to put the venv
p_django=$p_name  # The name of the django directory


# Set up the source directory
mkdir -p /srv
chown vagrant:vagrant /srv
ln -sfn /vagrant "$p_root"


echo 'Installing system packages'
apt-get update -y
# Install packages required for deployment
apt-get install -y $( cat "$p_root"/setup/apt-requirements.txt )
# Install packages required for developing
apt-get install -y git vim nano ncurses-term nfs-kernel-server nfs-common ipython

# Optional: install ElasticSearch (for higher-performance / more flexible search functionality)
#
# if ! command -v /usr/share/elasticsearch/bin/elasticsearch; then
#     apt-get install -y openjdk-6-jre-headless
#     echo "Downloading ElasticSearch..."
#     wget -q https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.11.deb
#     dpkg -i elasticsearch-0.90.11.deb
#     service elasticsearch start
# fi

# virtualenv global setup
pip install virtualenv


# Set up postgres
echo 'Adding postgres roles and databases'
as postgres psql <<<"CREATE USER ${p_name}_admin NOCREATEDB NOCREATEUSER PASSWORD 'ballroom'"
as postgres psql <<<"CREATE USER vagrant CREATEDB NOCREATEUSER PASSWORD 'ballroom'"
as postgres psql <<<"GRANT ${p_name}_admin TO vagrant"
as postgres psql <<<"CREATE DATABASE ${p_name}_admin ENCODING='UTF8' LC_CTYPE='en_AU.utf8' LC_COLLATE='en_AU.utf8' TEMPLATE=template0"


# Set up bash to automatically activate the virtualenv
# This is handy when logging in
echo 'Installing magic'
if ! grep -qxF 'source ~/.bashrc.vagrant' < "${v_home}/.bashrc" ; then
	cat >>"${v_home}/.bashrc" <<<"
source '${v_home}/.bashrc.vagrant'"
fi

cat >"${v_home}/.bashrc.vagrant" <<<"
cd '$p_root'
source '$p_venv/bin/activate'"


# The Makefile takes care of setting up an instance, once the system is capable
echo 'Running Makefile'
cd "$p_root"
as vagrant VENV_DIR="$p_venv" make -B all

chown vagrant:vagrant "${v_home}/.bashrc" "${v_home}/.bashrc.vagrant" "$p_venv"


# Set up the python environment
local_py="$p_django/settings/local.py"
if ! [[ -e "$local_py" ]] ; then
	echo "Making $local_py"
	cat > "$local_py" <<<"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${p_name}_admin',
        'USER': 'vagrant',
        'PASSWORD': 'ballroom',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = []
"
fi


# Django project setup
echo 'Finalising the Django install'
as vagrant bash -c "
set -e
source '${v_home}/.bashrc.vagrant'
python manage.py syncdb --noinput
python manage.py migrate --noinput
"