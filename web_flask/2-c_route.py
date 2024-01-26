#!/usr/bin/python3
"""
Hello world flask
"""
from flask import Flask
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
