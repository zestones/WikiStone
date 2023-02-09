import requests
import json

# Récupération des données depuis l'API
response = requests.get("https://data.culture.gouv.fr/api/records/1.0/search/?dataset=liste-et-localisation-des-musees-de-france&q=&facet=region_administrative&facet=departement")
data = json.loads(response.text)
print(data)
# Définition des propriétés pour chaque musée
properties = {
    "nom": {"type": "string"},
    "ville": {"type": "string"},
    "département": {"type": "string"},
    "région": {"type": "string"},
    "adresse": {"type": "string"}
}

# Création de modèles pour afficher les données de manière cohérente
template_musée = """
== {{{nom}}} ==

'''Ville:''' {{{ville}}}

'''Département:''' {{{département}}}

'''Région:''' {{{région}}}

'''Adresse:''' {{{adresse}}}
"""

template_région = """
== Musées de la région {{{région}}} ==

{{#ask: [[région::{{{région}}}]]
| ?nom
| ?ville
| ?département
| ?région
| ?adresse
| format=template
| template=template_musée
| limit=1000
}}
"""

# Boucle sur les données pour insérer chaque musée dans la wikibase
for record in data["records"]:
    # Création d'un item pour chaque musée
    item_data = {
        "labels": {
            "fr": record["fields"]["nom"]
        },
        "descriptions": {
            "fr": "Musée de France"
        },
        "claims": {
            "nom": {"value": record["fields"]["nom_du_musee"], "type": "string"},
            "ville": {"value": record["fields"]["ville"], "type": "string"},
            "département": {"value": record["fields"]["departement"], "type": "string"},
            "région": {"value": record["fields"]["region_administrative"], "type": "string"},
            "adresse": {"value": record["fields"]["adresse_du_musee"], "type": "string"}
        }
    }
    item_response = requests.post("http://localhost:8181/api.php", data={"action": "wbeditentity", "data": json.dumps(item_data), "format": "json"})

    if item_response.status_code != 200:
        print("Erreur lors de la création de l'item :", item_response.text)
    else:
        item_data = item_response.json()
        print("Item créé avec succès avec l'ID", item_data["entity"]["id"])

        # Ajout des données additionnelles à l'item
        claims = {
            "P17": {"value": "France", "type": "wikibase-item"},
            "P131": {"value": record["region_administrative"], "type": "wikibase-item"},
            "P131": {"value": record["departement"], "type": "wikibase-item"},
            "P276": {"value": record["adresse"], "type": "string"},
            "P969": {"value": record["latitude"], "type": "string"},
            "P970": {"value": record["longitude"], "type": "string"}
        }

        for prop, value in claims.items():
            statement_data = {
                "claims": [
                    {
                        "mainsnak": {
                            "snaktype": "value",
                            "property": prop,
                            "datavalue": {
                                "value": value["value"],
                                "type": value["type"]
                            }
                        },
                        "type": "statement",
                        "rank": "normal"
                    }
                ]
            }

            statement_response = requests.post(
                url=f"http://localhost/api/entity/{item_data['entity']['id']}/statements",
                headers="HEADERS",
                json=statement_data
            )

            if statement_response.status_code != 200:
                print("Erreur lors de l'ajout des données pour le musée :", record["nom_du_musee"], statement_response.text)
            else:
                print("Données ajoutées avec succès pour le musée :", record["nom_du_musee"])

