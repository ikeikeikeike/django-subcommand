
Django Subcommand
==================
Add sub command to the Django manage command.

Installation
=============

Edit settings.py

```python
INSTALLED_APPS = (
    "subcommand",
)
```

Usage
======

Generating the below command.

```bash
$ python manage.py startsubcommand APP_NAME SUBCOMMAND_NAME
```

Examples
=========

For more information, please see the [Example](https://github.com/ikeikeikeike/django-subcommand/tree/master/examples)

Setup
=====

```bash
$ pip install django-subcommand
```

Documentation
==============

[django-subcommand.rtfd.org](http://django-subcommand.rtfd.org)


License
=======
MIT License

