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
    python3 -m venv env # Linux or macOS
    ```

    If you're using Python 2, you need to install virtualenv first to have the virtual environment created.
    ```sh
    pip install virtualenv  # Windows
    sudo pip install virtualenv  # Linux or macOS
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
    source ./env/bin/activate # Linux or macOS
    ```

* Install Flask in the virtual environment
    ```sh
    (env) pip install Flask
    ```

* Exit the virtual environment
    ```sh
    deactivate
    ```

Core Function
-------------

* Source code example
    ```py
    from flask import Flask
    from flask import request, render_template, redirect, url_for

    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Welcome to Flask'
    
    @app.route('/url)
    def targetToUrl():
        return 'Hi there.'
    
    @app.route('/http-method', methods=['GET', 'POST'])
    def httpMethod():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        person = Person(name=name, age=age)
        return redirect(url_for('httpMethod'))

    return render_template('http-method.html')
    ```

* Run the program
    ```sh
    (env) flask run
    ```
    Open 'http://127.0.0.1:5000/' in brower
    'Welcome to Flask' will show on the webpage.

    Open 'http://127.0.0.1:5000/url' in brower
    'Hi there' will show up.

    Open 'http://127.0.0.1:5000/http-method' in brower
    The corresponding HTML file will be returned and rendered, if the POST request is triggered in the HTML, variable value can be passed via the url.

### Request-Response Handling

1. create URL via route()
2. the first request of '/' turns into the call of hello()
3. the function hello() returns a string text and rendered in the browser
4. the second request responses and renders the corresponding url content
5. the third requrst shows the different http methods and value be passed as parameter.

### Template Rendering

1. the render_template() function renders the html file located in the 'templates' folder which is located in the same root folder with the app.py
2. the template rendering engine is Jinja2, the Jinja2 program language can be embedded into the HTML
3. the values and arithmetic logic can also be insserted when rendering.
4. CSS and some JavaScript file can be stored in a folder called 'static', which is parallelly located with the 'templates' folder.


Database
--------

to be done

RESTful API
-----------

to be done

