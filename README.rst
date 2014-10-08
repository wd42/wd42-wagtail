dev42
===============================

Setting up for development
--------------------------

Get the code, and then ``make run``::

    $ git clone git@bitbucket.org:takeflight/dev42.git
    $ cd dev42
    $ make run

This will get the environment up and running.
You will need to create yourself a user account to log in with as well.
Open up another terminal, and run::

    $ vagrant ssh
    $ python manage.py createsuperuser
    $ exit

Every time you want to work on this project,
you can simply type ``make run`` again to start the development environment.

Deploying
---------

* Get the code and set up the environment::

        git clone git@bitbucket.org:takeflight/dev42.git
        cd dev42
        make all

* Make a database config::

        cp dev42/settings/local.py.example dev42/settings/local.py
        $EDITOR dev42/settings/local.py

* Either:
  * Import an existing database dump, or
  * Create a new, empty DB::

        python manage.py syncdb
        python manage.py migrate

* Use your choice of production daemon running/WSGI handler/voodoo incantations to
  connect the app with Nginx/Apache