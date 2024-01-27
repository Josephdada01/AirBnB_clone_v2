#!/usr/bin/python3
""" a script that starts a Flask web application:"""
from flask import Flask, escape


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
