#!/usr/bin/python3
"""
Airbnb flask now
"""
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def states():
    """Lists all states"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template("100-hbnb.html",
                           states=states, amenities=amenities,
                           places=places)


@app.teardown_appcontext
def tear_down(exception):
    """closing the storage"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
