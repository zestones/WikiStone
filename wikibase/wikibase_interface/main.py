from flask import Flask, jsonify, render_template, request
import json
import math

import os
import sys

# add the parent directory of main.py to Python path to enable import modules from the wikibase package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wikibase_request_api.python_wikibase import PyWikibase
from wikibase_injector.classifier.constants import CATEGORIES

# Authenticate with Wikibase
conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.json')
py_wb = PyWikibase(config_path=conf_path)  


app = Flask(__name__)


@app.route('/')
def index():
    sorted_categories = sorted(CATEGORIES, key=lambda x: 1 if x == 'Autre' else 0 if x != 'Autre' else -1)
    return render_template('index.html', data={}, categories=sorted_categories)

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


def parse_item_data(claims):
    result = {}
    prop_label = []
    for property_id, claim_list in claims.items():
        property_label = py_wb.Property().getPropertyLabel(property_id)
        prop_label.append(property_label)
        
        for claim in claim_list:
            if property_label == 'Location':
                result[property_label] = [float(claim.value.latitude), float(claim.value.longitude)]
            else:
                result[property_label] = str(claim.value)
                 
    return result, prop_label


@app.route('/result', methods=['GET'])
def display_item_page():
    item_id = request.args.get('id')

    item = py_wb.Item().get(entity_id=item_id)
    description = item.description.get()
    claims = item.claims.to_dict()

    title = item.label.get()
    data, prop_label = parse_item_data(claims)    
    return render_template('item.html', data=data, prop_label=prop_label, description=description, title=title)
