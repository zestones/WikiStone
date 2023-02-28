from wikibase_injector.data_formatter.label_properties import *

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

from bs4 import BeautifulSoup
import textwrap
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
    PROP_ANECDOTE[LABEL]: PROP_ANECDOTE,
    PROP_PRECISION_ON_PROTECTION[LABEL]: PROP_PRECISION_ON_PROTECTION
}


def extract_additional_infos(infos):
    # Match the details, comprendre, and anecdote patterns
    details_match = re.search(
        r'Voir : (.+?)(?=Comprendre)', infos, flags=re.DOTALL)
    comprendre_match = re.search(
        r'Comprendre : (.+?)(?=Anecdote|$)', infos, flags=re.DOTALL)
    anecdote_match = re.search(r'Anecdote : (.+)$', infos, flags=re.DOTALL)

    # Extract the matched strings
    details = details_match.group(1).strip() if details_match else ''
    comprendre = comprendre_match.group(1).strip() if comprendre_match else ''
    anecdote = anecdote_match.group(1).strip() if anecdote_match else ''

    return details, comprendre, anecdote


def extract_address_details(address):
    # Split the address into address, city, and postal code
    address_parts = [part.strip() for part in address.replace(
        '\r\n', '\n').replace('\r', '\n').split('\n') if part.strip()]

    return address_parts[0], address_parts[1], address_parts[2]


def scrap_data(soup):
    # Scrape the data
    results_div = soup.find("div", {"class": "resultatRecherche"})
    items = results_div.find_all("div", {"class": "blocResultat itemAnnuaire"})

    monuments = []
    for item in items:
        monument = {}
        # Extract the address
        address_div = item.find("div", {"class": "adresseStructure"})
        address = address_div.text.strip()
        address, city, postal_code = extract_address_details(address)

        # Extract the title/name
        title_div = item.find("p", {"class": "titreResultat"})
        title = title_div.text.strip()

        # Extract the additional information
        infos_div = item.find("div", {"class": "infosComplementaires"})
        infos = infos_div.text.strip()
        details, comprendre, anecdote = extract_additional_infos(infos)

        monument[PROP_NAME[LABEL]] = title

        # Don't add empty data
        if address:
            monument[PROP_ADDRESS[LABEL]] = address
        if city:
            monument[PROP_CITY[LABEL]] = city
        if postal_code:
            monument[PROP_POSTCODE[LABEL]] = postal_code
        if details:
            if len(details) > 400:
                monument[PROP_PRECISION_ON_PROTECTION[LABEL]] = textwrap.wrap(details, width=400)[0]
        if comprendre:
            if len(comprendre) > 250:
                monument[ITEM_DESCRIPTION] = textwrap.wrap(comprendre, width=250)[0]
        if anecdote:
            monument[PROP_ANECDOTE[LABEL]] = anecdote

        monuments.append(monument)

    return monuments


def retrieve_data():
    # Set up the Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Load the website
    url = "https://www.loire.fr/jcms/lw_1029499/fr/annuaire-du-patrimoine-et-monuments-de-la-loire"
    driver.get(url)

    # Find the search form and the "Valider" button
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".formulaireRecherche.zoneFormulaireGeo"))
    )

    inputs = form.find_elements(By.CSS_SELECTOR, "input[name]")
    data = {input.get_attribute("name"): input.get_attribute(
        "value") for input in inputs}
    data["structureSubmit"] = "Valider"

    # Submit the form and wait for the new page to load
    submit_button = form.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".blocResultat.itemAnnuaire"))
    )

    # Parse the HTML content of the new page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    monuments = scrap_data(soup)

    # Quit the driver and return the data
    driver.quit()
    return properties, monuments
