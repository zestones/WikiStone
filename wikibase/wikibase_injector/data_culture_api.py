import requests
from colorama import Fore, Style

# Define function to create properties if they don't exist
def create_property(py_wb, prop_label, prop_type):
    if not py_wb.Property().existProperty(prop_label):
        prop = py_wb.Property().create(prop_label, data_type=prop_type)
    else:
        prop_id = py_wb.Property().getPropertyId(prop_label)
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
    "website": "UrlValue",
    "location": "GeoLocation"
}

# Create the properties if they don't exist
def process_properties(py_wb):
    for prop_label, prop_type in properties.items():
        
        prop = create_property(py_wb, prop_label.capitalize(), prop_type)
        
        # Add label and description to property
        prop.label.set(prop_label.capitalize(), language="en")
        prop.description.set("Property for " + prop_label, language="en")

# retrieve the needed data
def retrieve_data(py_wb, data):
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

def inject_data(py_wb):
    process_properties(py_wb)

    # Retrieve data from API
    url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=liste-et-localisation-des-musees-de-france&q=&facet=region_administrative&facet=departement&refine.departement=Loire"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Error: {response.status_code}")
        
    data = response.json()
    museums = retrieve_data(py_wb, data)
    
    # Loop through museums and create Wikibase items with properties and values
    for museum in museums:
        exist_item, claim_list = False, {}
        
        if py_wb.Item().existItem(museum["name"]):
            item_id = py_wb.Item().getItemId(museum["name"])
            item = py_wb.Item().get(entity_id=item_id)
            
            exist_item = True
            claim_list = item.claims.to_dict()
        else : 
            item = py_wb.Item().create(museum["name"])

        print(Fore.MAGENTA + "====================== ITEM ======================")
        print(Fore.YELLOW + " |\tItem ID: " + Fore.WHITE +  item.entity_id)
        print(Fore.YELLOW + " |\tItem Label: ", Fore.WHITE,  item.label.get())
        print(Fore.YELLOW + " |\tItem Description: ", Fore.WHITE, item.description.get())
    

        # Loop through properties and add claims to item
        for prop_label, value in museum.items():

            prop_id = py_wb.Property().getPropertyId(prop_label.capitalize())
            prop = py_wb.Property().get(entity_id=prop_id.capitalize())

            # If property doesn't exist, skip it
            if prop is None:
                continue

            # Create value based on data type
            if properties[prop_label] == "StringValue":
                value = py_wb.StringValue().create(museum[prop_label])
            elif properties[prop_label] == "monolingualtext":
                value = py_wb.MonolingualTextValue().create(museum[prop_label], language="fr")
            elif properties[prop_label] == "quantity":
                value = py_wb.Quantity().create(museum[prop_label])
            elif properties[prop_label] == "wikibase-item":
                value = py_wb.Item().get(entity_id=museum[prop_label])
            elif properties[prop_label] == "GeoLocation":
                value = py_wb.GeoLocation().create(float(museum["location"].latitude), float(museum["location"].longitude))
            elif properties[prop_label] == "UrlValue":
                value = py_wb.UrlValue().create(("https://" + museum[prop_label]))
            else:
                continue
            
            # Update the existant claim
            if exist_item and prop_id in claim_list:
                for claim in claim_list[prop_id]:
                    if claim.value.__class__.__name__ == "GeoLocation":
                        if str(claim.value.latitude) != str(value.latitude) or str(claim.value.longitude) != str(value.longitude):
                            claim = item.claims.add(prop, value)
                            break
                        
                    elif str(claim.value).lower() != str(value).lower() :
                        claim = item.claims.add(prop, value)
                        break
            else:
                claim = item.claims.add(prop, value)

            print("---------- " + Fore.BLUE + "Statements" + Fore.WHITE +" ----------")
            print(Fore.YELLOW + " |\tClaim rank: ", Fore.WHITE, claim.rank)

            print("............ " + Fore.BLUE + "Property" + Fore.WHITE + " ............")
            print(Fore.YELLOW + " |\tProperty ID: ", Fore.WHITE, prop_id)
            print(Fore.YELLOW + " |\tProperty Label: ", Fore.WHITE, prop_label)
            print(Fore.YELLOW + " |\tClaim value: " , Fore.WHITE , claim.value)
            
            print()

        print(Style.RESET_ALL)
        break