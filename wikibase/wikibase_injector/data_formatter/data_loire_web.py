from label_properties import *
from bs4 import BeautifulSoup
import requests
import json
import re

# Define properties and data types
properties = {
    PROP_NAME[LABEL]: PROP_NAME,
    PROP_ADDRESS[LABEL]: PROP_ADDRESS,
    PROP_CITY[LABEL]: PROP_CITY,
    PROP_POSTCODE[LABEL]: PROP_POSTCODE,
    PROP_DEPARTEMENT[LABEL]: PROP_DEPARTEMENT,
    PROP_REGION[LABEL]: PROP_REGION,
    PROP_LOCATION[LABEL]: PROP_LOCATION,
    PROP_ANECDOTE[LABEL]: PROP_ANECDOTE
}

# Send a GET request to the website
url = "https://www.loire.fr/jcms/lw_1029499/fr/annuaire-du-patrimoine-et-monuments-de-la-loire"
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the form and the "Valider" button
form = soup.find("form", {"class": "formulaireRecherche zoneFormulaireGeo"})
button = form.find("button", {"name": "structureSubmit"})

# Get the URL of the page after clicking on the button
action = form.get("action")
data = {input.get("name"): input.get("value") for input in form.find_all("input")}
data["structureSubmit"] = "Valider"
response = requests.post(("https://www.loire.fr/" + action), data=data)

# Parse the HTML content of the new page
soup = BeautifulSoup(response.content, "html.parser")

# Scrape the data
results_div = soup.find("div", {"class": "resultatRecherche"})
items = results_div.find_all("div", {"class": "blocResultat itemAnnuaire"})

monuments = []
for item in items:
    monument = {}
    # Extract the address
    address_div = item.find("div", {"class": "adresseStructure"})
    address = address_div.text.strip()

    # Extract the title/name
    title_div = item.find("p", {"class": "titreResultat"})
    title = title_div.text.strip()

    # Extract the geolocation
    # geo_div = item.find("div", {"class": "geolocalisation"})
    # geo = geo_div.text.strip()

    # Extract the additional information
    infos_div = item.find("div", {"class": "infosComplementaires"})
    infos = infos_div.text.strip()

    # Match the details, comprendre, and anecdote patterns
    details_match = re.search(r'Voir : (.+?)(?=Comprendre)', infos, flags=re.DOTALL)
    comprendre_match = re.search(r'Comprendre : (.+?)(?=Anecdote|$)', infos, flags=re.DOTALL)
    anecdote_match = re.search(r'Anecdote : (.+)$', infos, flags=re.DOTALL)

    # Extract the matched strings
    details = details_match.group(1).strip() if details_match else ''
    comprendre = comprendre_match.group(1).strip() if comprendre_match else ''
    anecdote = anecdote_match.group(1).strip() if anecdote_match else ''

   # Split the address into address, city, and postal code
    address_parts = [part.strip() for part in address.replace('\r\n', '\n').replace('\r', '\n').split('\n') if part.strip()]
    address = address_parts[0]
    city = address_parts[1]
    postal_code = address_parts[2]

    monument[PROP_NAME[LABEL]] = title
    monument[PROP_ADDRESS[LABEL]] = address
    monument[PROP_CITY[LABEL]] = city
    monument[PROP_POSTCODE[LABEL]] = postal_code
    monument[PROP_DEPARTEMENT[LABEL]] = "Auvergne-Rhône-Alpes"
    monument[PROP_PRECISION_ON_PROTECTION[LABEL]] = details
    monument[ITEM_DESCRIPTION] = comprendre
    monument[PROP_ANECDOTE[LABEL]] = anecdote

    monuments.append(monument)


print(json.dumps(monuments, indent=2))
print(len(monuments))