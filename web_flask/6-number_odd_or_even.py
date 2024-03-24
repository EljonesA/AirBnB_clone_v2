#!/usr/bin/python3
''' Script that starts Flask web app '''

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    ''' returns “Hello HBNB!” '''
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def sub_route():
    ''' This performs routing to /hbnb '''
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    ''' Capture variable from url & use it in view function '''
    text = text.replace('_', ' ')
    return f"C {text}"


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text=None):
    ''' Provides default value "cool" for text variable if none provided '''
    # set default text variable value
    if text is None:
        text = 'is cool'
    text = text.replace('_', ' ')
    return f"Python {text}"


@app.route('/number/<int:n>', strict_slashes=False)
def check_n_type(n):
    ''' checking variable type in URLs. Ensures n is of type int '''
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def fetch_template(n):
    ''' Renders the html template 5-number.html '''
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def is_odd_or_even(n):
    ''' Returns only if n is int and states whether the int is odd/even  '''
    # check if n is odd or even
    if n % 2 == 0:
        text = 'even'
    else:
        text = 'odd'

    return render_template('6-number_odd_or_even.html', number=n, text=text)


if __name__ == '__main__':
    ''' Make the app available on all public IPs '''
    app.run(host='0.0.0.0')
