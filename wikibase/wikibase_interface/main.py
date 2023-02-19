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
    tmp = (request.args.get('results'))
    items_per_page = request.args.get('items_per_page', default=5, type=int)
    page = request.args.get('page', default=1, type=int)

    # Determine the range of items to display on the current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Slice the data to get only the items for the current page
    data_page = list(data.items())[start_index:end_index]

    return render_template('search-results.html', data=data_page, page=page, items_per_page=items_per_page, results=tmp)
