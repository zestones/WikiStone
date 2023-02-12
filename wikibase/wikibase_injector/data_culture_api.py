import requests
from wikibase_injector.label_properties import *

# Define properties and data types
properties = {
    PROP_LABEL_NAME: PROP_VALUE_STRING,
    PROP_LABEL_ADDRESS: PROP_VALUE_STRING,
    PROP_LABEL_CITY: PROP_VALUE_STRING,
    PROP_LABEL_POSTCODE: PROP_VALUE_STRING,
    PROP_LABEL_DEPARTEMENT: PROP_VALUE_STRING,
    PROP_LABEL_REGION: PROP_VALUE_STRING,
    PROP_LABEL_PHONE: PROP_VALUE_STRING,
    PROP_LABEL_WEBSITE: PROP_VALUE_URL,
    PROP_LABEL_LOCATION: PROP_VALUE_COORDINATE   
}


def construct_data_object(py_wb, data):
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

    return museums


def retrieve_data(py_wb):
    # Retrieve data from API
    url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=liste-et-localisation-des-musees-de-france&q=&facet=region_administrative&facet=departement&refine.departement=Loire"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Error: {response.status_code}")

    data = response.json()
    museums = construct_data_object(py_wb, data)
    
    return properties, museums
