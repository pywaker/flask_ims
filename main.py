"""
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <html><head><title>Flask App</title></head><body><h2>Hello World!</h2></body></html>
    """
