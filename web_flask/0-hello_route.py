#!/usr/bin/python3
''' Script that starts Flask web app '''

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    ''' returns “Hello HBNB!” '''
    return "Hello HBNB!"


if __name__ == '__main__':
    ''' Make the app available on all public IPs '''
    app.run(host='0.0.0.0')
