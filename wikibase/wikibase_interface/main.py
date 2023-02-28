from flask import Flask, render_template, request
import json
import math
import sys
import os

# add the parent directory of main.py to Python path to enable import modules from the wikibase package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wikibase_request_api.python_wikibase import PyWikibase

conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.json')
py_wb = PyWikibase(config_path=conf_path)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', data={}, first_render=True)


@app.route('/all-results', methods=['POST'])
def see_more():
    data = json.loads(request.form.get('results'))
    raw_data = request.form.get('results')

    items_per_page = request.form.get('items_per_page', default=5, type=int)
    page = request.form.get('page', default=1, type=int)

    # Calculate the number of pages
    num_items = len(data)
    num_pages = math.ceil(num_items / items_per_page)

    # Determine the range of items to display on the current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Slice the data to get only the items for the current page
    data_page = list(data.items())[start_index:end_index]

    return render_template('search-results.html', data=data_page, page=page, items_per_page=items_per_page, results=raw_data, num_pages=num_pages)

@app.route('/map')
def display_map():
    return render_template('map.html')