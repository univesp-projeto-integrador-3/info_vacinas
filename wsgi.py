# wsgy.py
import subprocess
import sys

from flask.cli import FlaskGroup

from project.server import create_app, db
from project.server.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

if __name__ == "__main__":
    cli = FlaskGroup(create_app=create_app)
    app.run()
