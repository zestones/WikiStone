import requests
import os
from dotenv import load_dotenv
from wikidataintegrator import wdi_core, wdi_login

from wikibaseintegrator.wbi_config import config as wbi_config

wbi_config['MEDIAWIKI_API_URL'] = 'http://localhost/api.php'
wbi_config['SPARQL_ENDPOINT_URL'] = 'http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql'
wbi_config['WIKIBASE_URL'] = 'http://wikibase.svc'

load_dotenv()

# Load the .env information
WIKIBASE_HOST = "http://localhost/api.php"

DB_USER = os.environ.get("MW_ADMIN_NAME")
DB_PASS = os.environ.get("MW_ADMIN_PASS")

# Load the data from the URL
data_url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=liste-et-localisation-des-musees-de-france&q=&facet=region_administrative&facet=departement"
response = requests.get(data_url)
museums_data = response.json()

# Login to Wikibase
login = wdi_login.WDLogin(DB_USER, DB_PASS, WIKIBASE_HOST)

# Define the data structure for the Wikibase item
item_structure = [
    wdi_core.WDItemID(value="Q{}".format(i), prop_nr="P31", is_reference=False)
    for i in range(1, len(museums_data) + 1)
]

# Create an instance of the WDItemEngine class
item_engine = wdi_core.WDItemEngine(mediawiki_api_url=WIKIBASE_HOST, sparql_endpoint_url=wbi_config['SPARQL_ENDPOINT_URL'])

# Create the items in Wikibase
item_response = item_engine.create_new_item(item_structure, data=None, entity_type='item')

# Check if the item creation was successful
if item_response.status_code != 200:
    print("Erreur lors de la création de l'item: {}".format(item_response.text))
else:
    print("Création de l'item réussie")
