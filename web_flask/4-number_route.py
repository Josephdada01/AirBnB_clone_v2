#!/usr/bin/python3
""" a script that starts a Flask web application"""
from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def display_hello():
    """ it display hbnb """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """ it will display hbnb """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_text(text):
    """
    display “C ” followed by the value of the text variable
    (replace underscore _ symbols with a space )
    """
    text = text.replace('_', ' ')
    return 'C {}'.format(escape(text))


@app.route('/python', strict_slashes=False)
@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python_text(text="is cool"):
    """
    display “Python ”, followed by the value of the text variable
    """
    normal_text = "{}".format(text)
    new_text = normal_text.replace('_', ' ')
    return 'Python {}'.format(escape(new_text))


@app.route('/number', strict_slashes=False)
@app.route('/number/', strict_slashes=False)
@app.route('/number/<n>', strict_slashes=False)
def display_n(n):
    """display “n is a number” only if n is an integer"""
    if type(n) == int:
        return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
