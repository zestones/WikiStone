from flask import Flask, render_template, request
import sys
import os
import json

# add the parent directory of main.py to Python path to enable import modules from the wikibase package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wikibase_request_api.python_wikibase import PyWikibase

conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.json')
py_wb = PyWikibase(config_path=conf_path)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', data={}, first_render=True)


@app.route('/all-results', methods=['GET'])
def see_more():

    data = json.loads(request.args.get('results'))
    
    return render_template('search-results.html', data=data)
