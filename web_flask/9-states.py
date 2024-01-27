#!/usr/bin/python3
"""
Airbnb flask now
"""
from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """Lists all states"""
    all_states = storage.all(State).values()
    return render_template("9-states.html", states=all_states, cities=0)


@app.route("/states/<id>", strict_slashes=False)
def state_by_id(id=None):
    """Lists all states"""
    all_states = storage.all(State).values()
    selected_state = None
    selected_state = list(filter(lambda x: x.id == id, all_states))
    return render_template("9-states.html", states=selected_state, cities=1)


@app.teardown_appcontext
def tear_down(exception):
    """closing the storage"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
