
from colorama import Style, Fore
import nbimporter
import threading
import colorama
import time
import sys
import os


from wikibase_injector.data_formatter.formatter.data_culture_api import retrieve_data as api_retrieve_data 
from wikibase_injector.data_formatter.formatter.data_clic_csv import retrieve_data as csv_retrieve_data 
from wikibase_injector.data_formatter.formatter.data_loire_web import retrieve_data as web_retrieve_data 
from wikibase_injector.data_injector.wiki_injector import inject_data
from wikibase_injector.classifier.constants import *

from wikibase_injector.classifier.classify_data import predict_monuments_category

# Initialize colorama
colorama.init()

def print_process(title, source):
    print(Fore.RED + "+" * 75)
    print(Fore.GREEN + "> {:^75}".format(title.upper() + " SOURCE : " + source))
    print(Fore.RED + "+" * 75, end="\n\n" + Fore.RESET)
   

def print_classify():
    animation = "|/-\\"
    idx = 0
    print(f"{Fore.CYAN}Classifying monument ", end="")
    sys.stdout.flush()

    while not event.is_set():
        print(f"{Style.BRIGHT}{Fore.BLUE}{animation[idx]}\b", end="", flush=True)
        idx = (idx + 1) % len(animation)
        time.sleep(0.1)
        
    print(f"{Fore.GREEN}Done", end="\n")


event = threading.Event()


# retrieve the data from the api : https://data.culture.gouv.fr/
def process_api_data(py_wb):
    print_process("API", "https://data.culture.gouv.fr/")
    properties, data = api_retrieve_data()
    inject_data(py_wb, data, properties)
    

# retrieve the data from the web : https://www.loire.fr/
def process_web_data(py_wb):
    print_process("SCRAP", "https://www.loire.fr/")
    properties, data = web_retrieve_data()

    thread = threading.Thread(target=print_classify)
    thread.start()

    data = predict_monuments_category(data)
    event.set()
    thread.join()

    inject_data(py_wb, data, properties)
    

def process_csv_data(py_wb):
    print_process("CSV", "https://dataclic.fr/")
    properties, data = csv_retrieve_data()

    thread = threading.Thread(target=print_classify)
    thread.start()

    data = predict_monuments_category(data)

    event.set()
    thread.join()
    inject_data(py_wb, data, properties)