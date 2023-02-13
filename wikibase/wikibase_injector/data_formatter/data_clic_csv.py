from wikibase_injector.data_formatter.label_properties import *
import textwrap
import csv

import json
# The proprties name and value
properties = {
    PROP_POSTCODE[LABEL]: PROP_POSTCODE,
    PROP_REGION[LABEL]: PROP_REGION,
    PROP_DEPARTEMENT[LABEL]: PROP_DEPARTEMENT,
    PROP_CITY[LABEL]: PROP_CITY,
    PROP_NAME[LABEL]: PROP_NAME,
    PROP_ADDRESS[LABEL]: PROP_ADDRESS,
    PROP_SIECLE[LABEL]: PROP_SIECLE,
    PROP_DATE_OF_PROTECTION[LABEL]: PROP_DATE_OF_PROTECTION,
    PROP_PRECISION_ON_PROTECTION[LABEL]: PROP_PRECISION_ON_PROTECTION,
    PROP_STATUT[LABEL]: PROP_STATUT,
    PROP_HISTORIQUE[LABEL]: PROP_HISTORIQUE,
    PROP_CONTACT[LABEL]: PROP_CONTACT,
    PROP_LOCATION[LABEL]: PROP_LOCATION,
}

# A mapping dictionary for the updated property names
mapping = {
    PROP_POSTCODE[LABEL]: "insee",
    PROP_REGION[LABEL]: PROP_REGION[LABEL],
    PROP_DEPARTEMENT[LABEL]: PROP_DEPARTEMENT[LABEL],
    PROP_CITY[LABEL]: "commune_1",
    PROP_NAME[LABEL]: "appellation_courante",
    PROP_ADDRESS[LABEL]: "adresse_1",
    PROP_SIECLE[LABEL]: "siecle",
    PROP_DATE_OF_PROTECTION[LABEL]: "date_de_protection",
    PROP_PRECISION_ON_PROTECTION[LABEL]: "precision_sur_la_protection",
    PROP_STATUT[LABEL]: "statut",
    ITEM_DESCRIPTION: "description",
    PROP_HISTORIQUE[LABEL]: "historique",
    PROP_CONTACT[LABEL]: "contact",
    PROP_LOCATION[LABEL]: "coordonnees",
}


def retrieve_data(): 
    # Open the CSV file and read the data
    monuments = []
    with open("../../data/monuments_historiques_departement42_2023-02-11.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract the relevant data using the updated properties mapping
            monument = {}
            for key, value in mapping.items():
                
                if key == PROP_LOCATION[LABEL] and (row["latitude"] != '' and row["longitude"] != ''):
                    monument[key] = [row["latitude"], row["longitude"]]
                elif row[value] != "":     
                    if key == ITEM_DESCRIPTION and len(row[value]) > 250:
                            monument[key] = textwrap.wrap(row[value], width=250)[0]
                    elif len(row[value]) > 400:
                            monument[key] = textwrap.wrap(row[value], width=400)[0]
                    else:
                        monument[key] = row[value]

            monuments.append(monument)
   
    return properties, monuments
