from flask import Flask, render_template, request
import sys
import os
import json

# add the parent directory of main.py to Python path to enable import modules from the wikibase package.
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from wikibase_request_api.python_wikibase import PyWikibase

conf_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../config.json')
py_wb = PyWikibase(config_path=conf_path)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', data={}, first_render=True)


def parse_query(items):
    parsed_items = {}
    for item in items:
        item_label = item.get("label")

        description = ""
        if "description" in item:
            description = item.get("description")

        parsed_items[item_label] = {
            "description": description
        }

    return parsed_items


@app.route('/search', methods=['POST'])
def search():

    query = request.form['query']
    raw_data = py_wb.Item().getItemIds(query)
    parsed_data = parse_query(raw_data)

    if len(parsed_data) > 7:
        trimmed_data = dict(list(parsed_data.items())[:7])
        return render_template('index.html', data=trimmed_data, see_more=(len(parsed_data) > 7))

    return render_template('index.html', data=parsed_data, see_more=(len(parsed_data) > 7))
