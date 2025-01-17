#!/usr/bin/python3
""" a script that starts a Flask web application"""
from flask import Flask, abort, render_template
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


@app.route('/number/<n>', strict_slashes=False)
def display_n(n):
    """display “n is a number” only if n is an integer"""
    try:
        n = int(n)
        return "{} is a number".format(n)
    except ValueError:
        abort(404)


@app.route('/number_template/<n>', strict_slashes=False)
def display_number_template(n):
    """display a HTML page only if n is an integer:"""
    try:
        n = int(n)
        return render_template('5-number.html', n=n)
    except ValueError:
        abort(404)


@app.route('/number_odd_or_even/<n>', strict_slashes=False)
def display_number_even_odd(n):
    """display a HTML page only if n is an integer"""
    try:
        n = int(n)
        return render_template('6-number_odd_or_even.html', n=n)
    except ValueError:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
