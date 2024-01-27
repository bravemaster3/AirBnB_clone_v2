#!/usr/bin/python3
"""
Airbnb flask now
"""
from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def list_states():
    """Lists all states"""
    all_states = storage.all(State).values()
    sorted_states = sorted(all_states, key=lambda x: x.name)
    return render_template("7-states_list.html", states=sorted_states)


@app.teardown_appcontext
def tear_down(exception):
    """closing the storage"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
