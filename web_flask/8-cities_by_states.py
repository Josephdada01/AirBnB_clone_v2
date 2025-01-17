#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models import *

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """function that list cities in state"""
    state_obj = storage.all(State)
    city_obj = storage.all(City)

    return render_template('8-cities_by_states.html',
                           state_obj=state_obj,
                           city_obj=city_obj)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    to perform cleanup or resource release operations
    after each request has been processed
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
