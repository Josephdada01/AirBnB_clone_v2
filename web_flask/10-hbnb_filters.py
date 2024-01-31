#!/usr/bin/python3
"""hbnb_filters module"""
from flask import Flask, render_template
from models import storage
from models import *

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """hbnb_filters: display a HTML with content of the airbnb clone static"""
    state_object = storage.all(State)
    city_object = storage.all(City)

    amenity_object = storage.all(Amenity)
    # sorted_amenities = sorted(amenities, key=lambda anemity: anemity.name)
    return render_template(
        '10-hbnb_filters.html',
        state_object=state_object,
        city_object=city_object,
        amenity_object=amenity_object,
        )


@app.teardown_appcontext
def teardown_db(exception):
    """To remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')