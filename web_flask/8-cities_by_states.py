#!/usr/bin/python3
"""
Airbnb flask now
"""
from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def list_cities_by_states():
    """Lists all states"""
    all_states = storage.all(State).values()
    # cities_by_states = {}
    # # sorted_states = sorted(all_states, key=lambda x: x.name)
    # for state in all_states:
    #     print(state.cities.name)
    #     state_name = state.name
    #     cities = [cities.to_dict() for city in state.cities]
    #     cities_by_states[state_name] = cities
    return render_template("8-cities_by_states.html", states=all_states)


@app.teardown_appcontext
def tear_down(exception):
    """closing the storage"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
