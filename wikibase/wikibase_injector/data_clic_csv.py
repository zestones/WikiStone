from wikibase_injector.label_properties import *
import textwrap
import csv


# The proprties name and value
properties = {
    PROP_LABEL_POSTCODE: PROP_VALUE_STRING,
    PROP_LABEL_REGION: PROP_VALUE_STRING,
    PROP_LABEL_DEPARTEMENT: PROP_VALUE_STRING,
    PROP_LABEL_CITY: PROP_VALUE_STRING,
    PROP_LABEL_NAME: PROP_VALUE_STRING,
    PROP_LABEL_ADDRESS: PROP_VALUE_STRING,
    PROP_LABEL_SIECLE: PROP_VALUE_STRING,
    PROP_LABEL_DATE_OF_PROTECTION: PROP_VALUE_STRING,
    PROP_LABEL_PRECISION_ON_PROTECTION: PROP_VALUE_STRING,
    PROP_LABEL_STATUT: PROP_VALUE_STRING,
    PROP_LABEL_HISTORIQUE: PROP_VALUE_STRING,
    PROP_LABEL_CONTACT: PROP_VALUE_STRING,
    PROP_LABEL_LOCATION: PROP_VALUE_COORDINATE,
    ITEM_DESCRIPTION: PROP_VALUE_STRING,

}

# A mapping dictionary for the updated property names
mapping = {
    PROP_LABEL_POSTCODE: "insee",
    PROP_LABEL_REGION: PROP_LABEL_REGION,
    PROP_LABEL_DEPARTEMENT: PROP_LABEL_DEPARTEMENT,
    PROP_LABEL_CITY: "commune_1",
    PROP_LABEL_NAME: "appellation_courante",
    PROP_LABEL_ADDRESS: "adresse_1",
    PROP_LABEL_SIECLE: "siecle",
    PROP_LABEL_DATE_OF_PROTECTION: "date_de_protection",
    PROP_LABEL_PRECISION_ON_PROTECTION: "precision_sur_la_protection",
    PROP_LABEL_STATUT: "statut",
    ITEM_DESCRIPTION: "description",
    PROP_LABEL_HISTORIQUE: "historique",
    PROP_LABEL_CONTACT: "contact",
    PROP_LABEL_LOCATION: "coordonnees",
}


def retrieve_data(py_wb):
    # Open the CSV file and read the data
    monuments = []
    with open("../data/monuments_historiques_departement42_2023-02-11.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract the relevant data using the updated properties mapping
            monument = {}
            for key, value in mapping.items():
                if key == PROP_LABEL_LOCATION:
                    monument[key] = py_wb.GeoLocation().create(
                        row["latitude"], row["longitude"])
                elif row[value] != "":     
                    if key == ITEM_DESCRIPTION and len(row[value]) > 250:
                            monument[key] = textwrap.wrap(row[value], width=250)[0]
                    elif len(row[value]) > 400:
                            monument[key] = textwrap.wrap(row[value], width=400)[0]
                    else:
                        monument[key] = row[value]

            monuments.append(monument)

    return properties, monuments
