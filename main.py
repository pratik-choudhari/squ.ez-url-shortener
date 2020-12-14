from flask import Flask, jsonify,render_template, request, redirect
import warnings
import re
import json
import random, string
from database import check_if_exists, insert_data, get_original_url, get_valid_combination
warnings.filterwarnings('ignore')
random.seed(10)

# app
app = Flask(__name__)


# routes


@app.route('/shorten', methods=['GET', 'POST'])
def results():
    url = request.args.get("url")
    if url:
        data = get_valid_combination(url)
        if data:
            response = app.response_class(
                response=json.dumps(data),
                status=200,
                mimetype='application/json'
            )
            return response
        else:
            return render_template("invalid.html")
    else:
        return render_template("index.html")


@app.route('/<cmpt_url>', methods=['GET', 'POST'])
def redirect_logic(cmpt_url):
    if not cmpt_url:
        return render_template('index.html')
    else:
        url = get_original_url(cmpt_url)
        if url:
            url = "".join(["http://www.", url])
            return redirect(url, code=302)
        else:
            return render_template("invalid.html")


@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port = 5000, debug=True)
