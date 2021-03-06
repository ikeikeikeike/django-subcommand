import os
from setuptools import setup

version = '0.3.2'
name = 'django-subcommand'
short_description = 'Add sub command to A Django manage command'
long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


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
    packages.append('.'.join(fullsplit(dirpath)))


setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=[
#       "Development Status :: 3 - Alpha",
       "Development Status :: 4 - Beta",
       "Framework :: Django",
       'Environment :: Console',
       "Environment :: Web Environment",
       "Intended Audience :: Developers",
       'License :: OSI Approved :: MIT License',
       "Programming Language :: Python :: 2.6",
       "Programming Language :: Python :: 2.7",
       'Topic :: Utilities',
       'Topic :: Software Development :: Libraries :: Python Modules',
    ],
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
    # include_package_data=True,
    # data_files=data_files,
    install_requires=[
        'inflection',
        'django-generate-scaffold',
    ]
)
