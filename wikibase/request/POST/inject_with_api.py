import requests
from create_property import create_property
from write_statement import write_statement
from create_entity import create_entity
import api_global

import sys

sys.path.append('../GET/')
from get_property import get_property_id

sys.path.append('../../authentification/')
from wiki_auth import authenticate

########################### WIKIBOT AUTH ##############################
login_info = authenticate()

csrf_token = login_info[0]
api_url = login_info[1]

########################## RETRIEVE JSON API ################################
# Fetch data from the API
url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=liste-et-localisation-des-musees-de-france&q=&facet=region_administrative&facet=departement&refine.departement=Loire"
response = requests.get(url)
data = response.json()
###############################################################

# Variables to store the entities and properties
museums = {}
labels, descriptions = [], []
property_labels = ["address",
                   "postal code", "city", "latitude", "longitude"]

property_datatypes = ["string", "string",
                      "string", "globe-coordinate", "globe-coordinate"]

entity_id_name = []

# Iterate through the records
for record in data["records"]:
    name = record["fields"]["nom_officiel_du_musee"]
    
    address = record["fields"]["adresse"]
    postal_code = record["fields"]["code_postal"]
    city = record["fields"]["commune"]
    
    latitude = record["fields"]["geolocalisation"][0]
    longitude = record["fields"]["geolocalisation"][1]

    # Store the entities
    museums[name] = {
        "address": address,
        "postal code": postal_code,
        "city": city,
        "latitude": latitude,
        "longitude": longitude
    }

    # Create the labels and descriptions
    labels = [{'language': 'en', 'string': name},
              {'language': 'fr', 'string': name}]
    
    descriptions = [
        {'language': 'en', 'string': f"Museum located at {address} with postal code {postal_code} in city {city} with latitude {latitude} and longitude {longitude}"}]

    # Create entities for each museum
    id_new_entity = create_entity(api_url, csrf_token, labels, descriptions)

    if id_new_entity != 'error':
        print("created item: " + str(name))
        print("assigned ID: " + str(id_new_entity))
        entity_id_name.append((id_new_entity, name))

# Check if properties exist
for i in range(len(property_labels)):
    property_exists = False
    property_url = api_url + '/property/' + property_labels[i]
    property_response = api_global.session.get(property_url)
    
    if property_response.status_code == 200:
        property_exists = True

    if not property_exists:
        create_property(api_url, csrf_token, property_labels[i], property_datatypes[i])


# Write statements for each entity
for entity in entity_id_name:
    entity_id = entity[0]
    entity_name = entity[1]

    museum = museums[entity_name]

    for property_label, property_datatype in zip(property_labels, property_datatypes):
        property_id = get_property_id(api_url, property_label)
        value = museum[property_label]
        
        if property_label == 'latitude' or property_label == 'longitude':
            value = [museum['latitude'], museum['longitude']] 
        
        write_statement(api_url, csrf_token, entity_id, property_id, value, property_datatype)
