# A integrated glance of full Flask usage

Flask is micro web framework written in Python, with no database abstraction layer or any other components where pre-existing third-party libraries provide common functions, meanwhile Flask supports large range of extentions which can make Flask serves as full functional framework.

The core functions of Flask itself is providing request-response handling and webpage rendering. These two functions are achieved by Werkzeug (a toolkit for Web Server Gateway Interface (WSGI) applications) and Jinja (a template engine, similar to the Django web framework) respectively.

Table of contents
-----------------

   * [Environment Configration](#environment-configration)
   * [Core Function](#core-function)
   * [Database](#database)
   * [RESTful API](#restful-api)

Environment Configration
------------------------

* Python installation
If you haven't had python ready on your computer, please check out this: https://www.python.org/downloads/

* Check Python version
```sh
python --version
```
or
```sh
python3 --version
```

* Create virtual environment
To create a isolated environment for python project, which means each project has its own dependencies and won't interfere each other.
```sh
python -m venv env  # Windows
python3 -m venv env # Linux 和 macOS
```

If you're using Python 2, you need to install virtualenv first to have the virtual environment created.
```sh
pip install virtualenv  # Windows
sudo pip install virtualenv  # Linux 或 macOS
```
Then create the virtual environment:
```sh
virtualenv env
```

* Activate the virtual environment
```sh
env\Scripts\activate  # Windows
```
```sh
source ./env/bin/activate
```

* Install Flask in the virtual environment
```sh
pip install Flask
```

* Exit the virtual environment
```sh
deactivate
```

Core Function
-------------

to be done

Database
--------

to be done

RESTful API
-----------

to be done

