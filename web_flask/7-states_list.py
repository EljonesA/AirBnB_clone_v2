#!/usr/bin/python3
"""Script to start a Flask web application"""

from flask import Flask, render_template
import os
import sys

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (one level up)
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the Python path
sys.path.append(parent_dir)

from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    ''' return html page with list of states '''
    states = storage.all().values()
    sorted_states = sorted(states, key=lambda state: state.name)

    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown_db(exception):
    ''' close current SQLAlchemy Session after @ request '''
    # storage.close()


if __name__ == '__main__':
    ''' Make app available on IP 0.0.0.0 '''
    app.run(host='0.0.0.0', port=5000)
