import os
import requests
from python_wikibase import PyWikibase
from write_url import write_url
import sys
sys.path.append('./../authentification/')
from wiki_auth import authenticate

login_infos = authenticate()
edit_token = login_infos[0]
wiki_api_url = login_infos[1]


# Authenticate with Wikibase
conf_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'config.json')
py_wb = PyWikibase(config_path=conf_path)


def get_property_id(property_label):
    params = {
        "action": "wbsearchentities",
        "language": "en",
        "format": "json",
        "type": "property",
        "limit": 1,
        "search": property_label
    }

    response = requests.get(wiki_api_url, params=params).json()

    if "success" in response and response["success"] == 1:
        if "search" in response and len(response["search"]) > 0:
            return response["search"][0]["id"]

    return None


# Check if properties exist
def exist_property(prop_label):
    prop_exists = False

    prop_url = wiki_api_url + '/property/' + prop_label
    response = requests.get(prop_url)

    if response.status_code == 200:
        prop_exists = True

    return prop_exists


# Define function to create properties if they don't exist
def create_property(prop_label, prop_type):
    if not exist_property(prop_label):
        prop = py_wb.Property().create(prop_label, data_type=prop_type)
    else:
        prop_id = get_property_id(prop_label)
        prop = py_wb.Property().get(entity_id=prop_id)

    return prop


# Define properties and data types
properties = {
    "name": "StringValue",
    "address": "StringValue",
    "city": "StringValue",
    "postcode": "StringValue",
    "departement": "StringValue",
    "region": "StringValue",
    "phone": "StringValue",
    "website": "Url",
    "location": "GeoLocation"
}

# Create properties if they don't exist
for prop_label, prop_type in properties.items():
    if prop_type == "GeoLocation":
        prop = create_property(prop_label.capitalize(), "GeoLocation")
    else:
        prop = create_property(prop_label.capitalize(), prop_type)

    # Add label and description to property
    prop.label.set(prop_label.capitalize(), language="en")
    prop.description.set("Property for " + prop_label, language="en")

# Retrieve data from API
url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=liste-et-localisation-des-musees-de-france&q=&facet=region_administrative&facet=departement&refine.departement=Loire"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    museums = []

    # Loop through records and add to museums list
    for record in data["records"]:
        museum = {}

        # Get values for each property
        museum["name"] = record["fields"]["nom_officiel_du_musee"]
        museum["address"] = record["fields"]["adresse"]
        museum["city"] = record["fields"]["commune"]
        museum["postcode"] = record["fields"]["code_postal"]
        museum["departement"] = record["fields"]["departement"]
        museum["region"] = record["fields"]["region_administrative"]
        museum["phone"] = record["fields"]["telephone"]
        museum["website"] = record["fields"]["url"]
        museum["location"] = py_wb.GeoLocation().create(
            record["fields"]["latitude"], record["fields"]["longitude"])

        # Add museum to museums list
        museums.append(museum)

    # Loop through museums and create Wikibase items with properties and values
    for museum in museums:
        item = py_wb.Item().create(museum["name"])

        # Loop through properties and add claims to item
        for prop_label, value in museum.items():

            print("=>" + prop_label)
            prop_id = get_property_id(prop_label.capitalize())
            print("-->" + str(prop_id))
            prop = py_wb.Property().get(entity_id=prop_id.capitalize())

            # If property doesn't exist, skip it
            if prop is None:
                continue

            # Create value based on data type
            if properties[prop_label] == "StringValue":
                value = py_wb.StringValue().create(museum[prop_label])
            elif properties[prop_label] == "monolingualtext":
                value = py_wb.MonolingualTextValue().create(
                    museum[prop_label], language="fr")
            elif properties[prop_label] == "quantity":
                value = py_wb.Quantity().create(museum[prop_label])
            elif properties[prop_label] == "wikibase-item":
                value = py_wb.Item().get(entity_id=museum[prop_label])
            elif properties[prop_label] == "GeoLocation":
               value = py_wb.GeoLocation().create(
                float(museum["location"].latitude), float(museum["location"].longitude))

            # elif properties[prop_label] == "Url":
            #     write_url(wiki_api_url, item.get().entity_id,prop_id, museum[prop_label], edit_token)
            #     continue
            # elif properties[prop_label] == "time":
            #     value = py_wb.TimeValue().create(museum[prop_label])
            else:
                continue
                # value = py_wb.StringValue().create(museum[prop_label])

            # Add claim to item
            claim = item.claims.add(prop, value)
        break
else:
    print("Error:", response.status_code)
