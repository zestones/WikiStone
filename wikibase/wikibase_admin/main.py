from colorama import Fore, Style
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


def usage(program_name):
    print(f"{Fore.GREEN}Usage: python {program_name} [OPTIONS]{Style.RESET_ALL}")
    print("")
    
    print(Style.BRIGHT + Fore.BLUE + "Options:" + Style.RESET_ALL)
    print(f"  {Fore.CYAN}-h, --help{Style.RESET_ALL}\tShow this help message and exit")
    print(f"  {Fore.CYAN}-w, --web{Style.RESET_ALL}\tRun the web application")
    print(f"  {Fore.CYAN}-a, --app{Style.RESET_ALL}\tRun the desktop application")
    
    print("")
    sys.exit(1)


@eel.expose
def process_api_data():
    properties, data = data_culture_api.retrieve_data()
    inject_data(py_wb, data, properties)


@eel.expose
def process_csv_data():
    properties, data = data_clic_csv.retrieve_data()
    inject_data(py_wb, data, properties)
   
    
@eel.expose
def process_web_data():
    properties, data = data_loire_web.retrieve_data()
    inject_data(py_wb, data, properties)

@eel.expose
def updateProperty(id, label, description): 
    prop = py_wb.Property().get(entity_id=id)
    
    prop.label.set(label, language=py_wb.language)
    prop.description.set(description, language=py_wb.language)

@eel.expose
def deleteProperty(id):
    prop = py_wb.Property().get(entity_id=id)
    prop.delete()

def main(argv):
    
    # Launching the app in the browser
    if '-w' in argv or '--web' in argv:
        eel.start('index.html', mode='chrome-app', port=8000)
    # Launching the app as a desktop app
    elif '-a' in argv or '--app' in argv:
        eel.start('index.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron.exe', '.'])
    else:
        usage(argv[0])

if __name__ == '__main__':
    main(sys.argv)
