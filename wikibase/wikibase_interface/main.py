from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/search', methods=['POST'])
# def search():
#     query = request.form['query']
#     results = search_wikibase(query)
#     return render_template('results.html', results=results)