#!/usr/bin/python3
"""
Hello world flask
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """greetings from HBNB"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def whoami():
    """greetings from HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def howami(text=None):
    """Complete: C is ?"""
    return f"C {text.replace('_', ' ')}"


@app.route("/python", strict_slashes=False)
@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def always_cool(text="is cool"):
    """Complete: Python is ?"""
    return f"Python {text.replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def number_only(n=None):
    """Complete: is n a number?"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n=None):
    """Complete: is n a number?"""
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
