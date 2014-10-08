VAR_DIRS := var
VAR_DIRS := ${VAR_DIRS} var/www
VAR_DIRS := ${VAR_DIRS} var/www/static
VAR_DIRS := ${VAR_DIRS} var/www/media var/www/media/uploads
VAR_DIRS := ${VAR_DIRS} var/cache
VAR_DIRS := ${VAR_DIRS} var/logs

SECRETS_PY := dev42/settings/secrets.py

VENV_DIR ?= venv
ENVIRONMENT ?= develop
DJANGO_SETTINGS_MODULE := dev42/settings/${ENVIRONMENT}
PIP_REQUIREMENTS := setup/pip-requirements/${ENVIRONMENT}.txt
export DJANGO_SETTINGS_MODULE

all: dev permissions
dev: secrets virtualenv

permissions: var_dirs secrets
	sudo chown -R www-data ${VAR_DIRS}
	sudo chgrp -R staff ${VAR_DIRS}
	sudo chmod -R u=rw,g=rw,o= ${VAR_DIRS}
	sudo chmod -R u+X,g+sX ${VAR_DIRS}
	sudo chown www-data ${SECRETS_PY}
	sudo chgrp staff ${SECRETS_PY}
	sudo chmod u=r,g=r,o= ${SECRETS_PY}

var_dirs: | ${VAR_DIRS}

${VAR_DIRS}:
	mkdir -p $@

secrets: ${SECRETS_PY}

${SECRETS_PY}:
	echo '""" Secrets for this instance """' > $@
	rm -f $@
	@echo "SECRET_KEY = '$(shell head -c36 /dev/urandom | base64 )'" > $@

virtualenv: $(VENV_DIR)
$(VENV_DIR): ${PIP_REQUIREMENTS}
	virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r ${PIP_REQUIREMENTS}
	touch $(VENV_DIR)

.PHONY: var_dirs permissions secrets

# Compiling front end files
# -------------------------
# Making the assets means making all the individual asset types
.PHONY: assets
	$(MAKE) -C dev42/website/static

# Running the app via Vagrant
# ---------------------------

.PHONY: run
run:
	vagrant up
	@echo "Visit http://localhost:1100/"
	vagrant ssh -c "source ~/.bashrc.vagrant; python manage.py runserver 0.0.0.0:1100"