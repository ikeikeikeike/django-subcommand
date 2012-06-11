import os
from setuptools import setup

version = '0.0.1'
name = 'django-subcommand'
short_description = 'Add sub command to A Django manage command'
long_description = """\
``Add sub command to A Django manage command.``

Description
===========

Requirements
============
* django
* django_compressor
* inflection
* django-generate-scaffold (optional)

Features
========


Setup
=====


Installation
~~~~~~~~~~~~


History
========
0.x (2012-xx-xx)
~~~~~~~~~~~~~~~~
* first release

License
=======
MIT License
"""


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
extensions_dir = 'subcommand'

for dirpath, dirnames, filenames in os.walk(extensions_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


classifiers = [
   "Development Status :: 3 - Alpha",
#   "Development Status :: 4 - Beta",
   "Framework :: Django",
   "Environment :: Web Environment",
   "Intended Audience :: Developers",
   "Programming Language :: Python",
   'Topic :: Utilities',
   'License :: OSI Approved :: MIT License',
]

setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    keywords=[
        'javascript',
        'coffeescript',
        'django',
        'command'
    ],
    author='Tatsuo Ikeda',
    author_email='jp.ne.co.jp at gmail',
    url='https://github.com/ikeikeikeike/django-subcommand',
    license='MIT License',
    packages=packages,
    data_files=data_files,
    py_modules=['subcommand'],
    install_requires=[
        'django',
        'django-generate-scaffold',
        'django_compressor',
        'inflection'
    ]
)
