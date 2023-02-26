import eel
import sys
import os
# add the parent directory of main.py to Python path to enable import modules from the wikibase package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wikibase_request_api.python_wikibase import PyWikibase
from wikibase_injector.data_injector.wiki_injector import inject_data
import wikibase_injector.data_formatter.data_culture_api as data_culture_api
import wikibase_injector.data_formatter.data_clic_csv as data_clic_csv
import wikibase_injector.data_formatter.data_loire_web as data_loire_web


# Authenticate with Wikibase
conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.json')
py_wb = PyWikibase(config_path=conf_path)  

# Set web files folder
eel.init('web')

@eel.expose
def process_api_data():
    properties, data = data_culture_api.retrieve_data()
    inject_data(py_wb, data, properties)

@eel.expose
def process_csv_data(py_wb):
    properties, data = data_clic_csv.retrieve_data()
    inject_data(py_wb, data, properties)
    
@eel.expose
def process_web_data(py_wb):
    properties, data = data_loire_web.retrieve_data()
    inject_data(py_wb, data, properties)

def main(argv):
    
    if '-w' in argv or '--web' in argv:
        eel.start('index.html', mode='electron .')
    elif '-a' in argv or '--app' in argv:
        eel.start('hello.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron.exe', '.'])
    else:
        print('Usage: main.py [-w|--web] [-a|--app]')
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
