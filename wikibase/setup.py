import os
import sys

from wikibase_request_api import PyWikibase
from wikibase_injector.data_culture_api import inject_data

# main function
def main(argv):

    # Authenticate with Wikibase
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    py_wb = PyWikibase(config_path=conf_path)  
    inject_data(py_wb)


if __name__ == '__main__':
    main(sys.argv)