# coding: utf-8
import os

from flask import Flask
from flask import request
from flask import jsonify

from loadmodel import *

app = Flask(__name__)

@app.route('/')
def Request():
    if request.args and 'label' in request.args:
        string = request.args.get('label')
        num = request.args.get('num')
        sentence = request.args.get('sentence')
        return find_(string, num, sentence)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
