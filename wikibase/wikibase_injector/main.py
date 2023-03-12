import os
import sys
import getopt
import nbimporter
import colorama
from colorama import Style, Fore

# add the parent directory of main.py to Python path to enable import modules from the wikibase package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wikibase_request_api.python_wikibase import PyWikibase
import wikibase_injector.data_formatter.data_culture_api as api
import wikibase_injector.data_formatter.data_clic_csv as csv
import wikibase_injector.data_formatter.data_loire_web as web

# Display program usage
def usage(program_name):
    print(f"{Fore.GREEN}Usage: python {program_name} [OPTIONS]{Style.RESET_ALL}")
    print("")
    
    print(Style.BRIGHT + Fore.BLUE + "OPTIONS:", Style.RESET_ALL)
    print(f"  {Fore.CYAN}-h, --help{Style.RESET_ALL}\t\tShow this help message and exit")
    print(f"  {Fore.CYAN}-p, --process{Style.RESET_ALL}\t\tProcess all available data sources (API, CSV, Web Scraping)")
    print(f"  {Fore.CYAN}-a, --api{Style.RESET_ALL}\t\tProcess data from API only")
    print(f"  {Fore.CYAN}-c, --csv{Style.RESET_ALL}\t\tProcess data from CSV file only")
    print(f"  {Fore.CYAN}-s, --scrap{Style.RESET_ALL}\t\tProcess data from Web Scraping only")
    
    print("")
    sys.exit(0)


# main function
def main(argv):

    # get the option 
    try:
        opts, _ = getopt.getopt(argv[1:], 'hpcas', ['help', 'process', 'csv', 'api', 'scrapp'])
    except getopt.GetoptError: usage(argv[0])
    
    if (len(argv) < 2): usage(argv[0])
    
    # Authenticate with Wikibase
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.json')
    py_wb = PyWikibase(config_path=conf_path)  
    
    for opt, _ in opts:
        if opt in ('-h', '--help'):
            usage(argv[0])
        
        elif opt in ('-p', '--process'):
            api.process_api_data(py_wb)
            csv.process_csv_data(py_wb)
            web.process_web_data(py_wb)
            
        elif opt in ('-a', '--api'):
            api.process_api_data(py_wb)
        
        elif opt in ('-c', '--csv'):
            csv.process_csv_data(py_wb)
        
        elif opt in ('-s', '--scrap'):
            web.process_web_data(py_wb)
        
    
if __name__ == '__main__':
    main(sys.argv)