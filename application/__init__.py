from flask import Flask

# Create flask app
app = Flask(__name__)

# Circular import to properly create app
from application import main