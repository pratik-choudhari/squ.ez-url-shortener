import os
import warnings
import random

from flask import Flask, render_template, request, redirect
from database import get_original_url, get_valid_combination


warnings.filterwarnings('ignore')
random.seed(10)


# app
app = Flask(__name__)


# shortening route
@app.route('/shorten', methods=['GET', 'POST'])
def shorten():
    url = request.form['url']
    if url:
        data = get_valid_combination(url)
        if data:
            return render_template("success.html", shrt=data)
        return render_template("invalid.html")
    return render_template("index.html")


# redirection route
@app.route('/<cmpt_url>', methods=['GET', 'POST'])
def redirect_logic(cmpt_url):
    if not cmpt_url:
        return render_template('index.html')     
    url = get_original_url(cmpt_url, True)
    if url:
        url = "".join(["http://www.", url])
        return redirect(url, code=302)
    return render_template("invalid.html")


# index route
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template("index.html")


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = "production"
    app.run(host= '0.0.0.0',port = 5000, debug=False)
