import requests
from wikibase_injector.data_formatter.label_properties import *

# Define properties and data types
properties = {
    PROP_NAME[LABEL]: PROP_NAME,
    PROP_ADDRESS[LABEL]: PROP_ADDRESS,
    PROP_CITY[LABEL]: PROP_CITY,
    PROP_POSTCODE[LABEL]: PROP_POSTCODE,
    PROP_DEPARTEMENT[LABEL]: PROP_DEPARTEMENT,
    PROP_REGION[LABEL]: PROP_REGION,
    PROP_PHONE[LABEL]: PROP_PHONE,
    PROP_WEBSITE[LABEL]: PROP_WEBSITE,
    PROP_LOCATION[LABEL]: PROP_LOCATION   
}

def construct_data_object(data):
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
        museum["location"] = [record["fields"]["latitude"], record["fields"]["longitude"]]

        # Add museum to museums list
        museums.append(museum)

    return museums


def retrieve_data():
    # Retrieve data from API
    url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=liste-et-localisation-des-musees-de-france&q=&facet=region_administrative&facet=departement&refine.departement=Loire"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Error: {response.status_code}")

    data = response.json()
    museums = construct_data_object(data)
    
    return properties, museums
