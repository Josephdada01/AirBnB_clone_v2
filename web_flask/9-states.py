#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models import *

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def display_states_cities(state_id=None):
    """listing cities inside of state"""
    state_object = storage.all(State)
    city_object = storage.all(City)

    if "State.{}".format(state_id) in state_object:
        state = state_object["State.{}".format(state_id)]
        return render_template('9-states.html',
                               state_object=state_object,
                               city_object=city_object,
                               state_id=state_id,
                               state=state)
    return render_template('9-states.html',
                           state_object=state_object,
                           city_object=city_object,
                           state_id=state_id,
                           state=state)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    to perform cleanup or resource release operations
    after each request has been processed
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
