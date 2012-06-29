

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
$ python manage.py generate -h
```

```bash
$ python manage.py destroy -h
```

Examples
=========

For more information, please see the [Example](https://github.com/ikeikeikeike/django-subcommand/tree/master/examples)


Setup
=====

```bash
$ pip install django-subcommand
```

License
=======
MIT License

