from colorama import Style, Fore
import threading
import colorama
import time
import sys
import os

# add the parent directory of main.py to Python path to enable import modules from the wikibase package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wikibase_injector.classifier.constants import *
from wikibase_injector.classifier.classify_data import predict_monuments_category
from wikibase_injector.data_injector.wiki_injector import inject_data

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