#wd42 & #pd42 website
===============================

Setting up for development
--------------------------

Get the code, and then ``make run``::

    $ git clone git@github.com:wd42/wd42-wagtail.git
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
