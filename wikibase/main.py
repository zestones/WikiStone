import os
import sys

from wikibase_request_api import PyWikibase
from wikibase_injector.wiki_injector import inject_data
import wikibase_injector.data_culture_api as data_culture_api
import wikibase_injector.data_clic_csv as data_clic_csv


# main function
def main(argv):

    # Authenticate with Wikibase
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    py_wb = PyWikibase(config_path=conf_path)  
    
    # retrieve the data
    properties, data = data_clic_csv.retrieve_data(py_wb)
    inject_data(py_wb, data, properties)
    
    properties, data = data_culture_api.retrieve_data(py_wb)
    inject_data(py_wb, data, properties)
    
if __name__ == '__main__':
    main(sys.argv)