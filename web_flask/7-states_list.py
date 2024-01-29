#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models import *

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """a function that render lists of states"""
    state_obj = storage.all(State)
    return render_template('7-states_list.html', state_obj=state_obj)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    to perform cleanup or resource release operations
    after each request has been processed
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
