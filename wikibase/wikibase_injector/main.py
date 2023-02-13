import os
import sys
from colorama import Fore, Style

# add the parent directory of main.py to Python path to enable import modules from the wikibase package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wikibase_request_api.python_wikibase import PyWikibase
from wikibase_injector.data_injector.wiki_injector import inject_data
import wikibase_injector.data_formatter.data_culture_api as data_culture_api
import wikibase_injector.data_formatter.data_clic_csv as data_clic_csv


def print_process(title, source):
    print(Fore.RED + "+" * 75)
    print(Fore.GREEN + "> {:^75}".format(title.upper() + " SOURCE : " + source))
    print(Fore.RED + "+" * 75, end="\n\n" + Fore.RESET)

# main function
def main(argv):

    # Authenticate with Wikibase
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.json')
    py_wb = PyWikibase(config_path=conf_path)  
    
    # retrieve the data from the api : https://data.culture.gouv.fr/
    print_process("API", "https://data.culture.gouv.fr/")
    properties, data = data_culture_api.retrieve_data()
    inject_data(py_wb, data, properties)
    
    # retrieve the data from the csv : https://dataclic.fr/
    print_process("CSV", "https://dataclic.fr/")
    properties, data = data_clic_csv.retrieve_data()
    inject_data(py_wb, data, properties)
    
if __name__ == '__main__':
    main(sys.argv)