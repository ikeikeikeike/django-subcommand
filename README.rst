
Django Subcommand
==================
Add sub command to A Django manage command.


Installation
~~~~~~~~~~~~

Edit settings.py ::

    INSTALLED_APPS = (
        "subcommand",
    )

Usage
======

Generating the below command.

::

    $ python manage.py generate -h

    $ python manage.py destroy -h


Examples
=========

For more information, please see the `Example <https://github.com/ikeikeikeike/django-subcommand/tree/master/examples>`_


Setup
=====

::

    $ pip install django-subcommand


License
========
MIT License
