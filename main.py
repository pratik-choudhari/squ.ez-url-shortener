from flask import Flask, jsonify,render_template, request
import warnings
import re
import json
import random, string
import sqlite3
warnings.filterwarnings('ignore')
random.seed(10)

# app
app = Flask(__name__)
conn = sqlite3.connect("url.db")

# generate url
def get_valid_combination(url: str)-> str:
    regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"""
    res = re.findall(regex, url)
    data = "Invalid URL"
    if res:
        flag = True
        while flag:
            shrt = ''.join(random.choice(string.ascii_letters) for _ in range(8))
            query = f'''SELECT COUNT(ID) FROM URLS WHERE ID={shrt}'''
            db_res = conn.execute(query)
            if [i[0] for i in db_res] == [0]:
                query = f'''INSERT INTO URLS (ID, ORIGINAL, VISITS) VALUES ({shrt}, {url}, 0);'''
                db_res = conn.execute(query)
                if not db_res:
                    return "Error inserting data"
                data = "".join(["localhost/", shrt])
                flag = False
                break
    return data

# routes
@app.route('/', methods=['GET','POST'])
def homepage():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def results():
    url = request.args.get("url")
    data = get_valid_combination(url)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port = 5000, debug=True)
