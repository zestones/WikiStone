from wikibase_injector.label_properties import *
from colorama import Fore, Style

# Print the details of a property
def print_property(prop, title):
    print(Fore.YELLOW + "_________________________________________")
    print(Fore.BLUE +  "|========================================|")
    print(Fore.BLUE + "| " + " " * 12 + " " + Fore.MAGENTA + title + " ")
    print(Fore.BLUE + "|" + "=" * 40 + "|")
    print(Fore.CYAN + "| Property Id : " + Fore.WHITE + str(prop.entity_id))
    print(Fore.CYAN + "| Label: " + Fore.WHITE + str(prop.label))
    print(Fore.CYAN + "| Data Type : " + Fore.WHITE + str(prop.data_type))
    # print(Fore.CYAN + "| Description: " + Fore.WHITE + str(prop.description))
    print(Fore.YELLOW + "------------------------------------------" + Style.RESET_ALL)

# Print the details of an item
def print_item(item):
    print(Fore.MAGENTA + "====================== ITEM ======================")
    print(Fore.YELLOW + " |\tItem ID: " + Fore.WHITE +  item.entity_id)
    print(Fore.YELLOW + " |\tItem Label: ", Fore.WHITE,  item.label.get())
    print(Fore.YELLOW + " |\tItem Description: ", Fore.WHITE, item.description.get())

# Print the details of a statement
def print_statement_details(claim, prop_id, prop_label):
    print("---------- " + Fore.BLUE + "Statements" + Fore.WHITE +" ----------")
    print(Fore.YELLOW + " |\tClaim rank: ", Fore.WHITE, claim.rank)

    print("............ " + Fore.BLUE + "Property" + Fore.WHITE + " ............")
    print(Fore.YELLOW + " |\tProperty ID: ", Fore.WHITE, prop_id)
    print(Fore.YELLOW + " |\tProperty Label: ", Fore.WHITE, prop_label)
    print(Fore.YELLOW + " |\tClaim value: " , Fore.WHITE , claim.value)

# Define function to create properties if they don't exist
def create_property(py_wb, prop_label, prop_type):
    if not py_wb.Property().existProperty(prop_label):
        prop = py_wb.Property().create(prop_label, data_type=prop_type)
        print_property(prop, "NEW PROPERTY")        
    else:
        prop_id = py_wb.Property().getPropertyId(prop_label)
        prop = py_wb.Property().get(entity_id=prop_id)
        print_property(prop, "FOUND PROPERTY")

    return prop

# Create the properties if they don't exist
def process_properties(py_wb, properties):
    for prop_label, prop_type in properties.items():
        prop_label_formatted = prop_label.replace("_", " ")
        
        prop = create_property(py_wb, prop_label_formatted.capitalize(), prop_type)
        
        ### TODO : Update only if needed ###
        # Add label and description to property
        prop.label.set(prop_label_formatted.capitalize(), language=py_wb.language)
        prop.description.set("Property for " + prop_label_formatted, language=py_wb.language)
        ###### TODO ######

# Create the value for the claim
def create_claim_value(py_wb, properties, prop_label, object):
    value = None
    
    if properties[prop_label] == PROP_VALUE_STRING:
        value = py_wb.StringValue().create(object[prop_label])
    elif properties[prop_label] == "monolingualtext":
        value = py_wb.MonolingualTextValue().create(object[prop_label], language="fr")
    elif properties[prop_label] == "quantity":
        value = py_wb.Quantity().create(object[prop_label])
    elif properties[prop_label] == "wikibase-item":
        value = py_wb.Item().get(entity_id=object[prop_label])
    elif properties[prop_label] == PROP_VALUE_COORDINATE:
        value = py_wb.GeoLocation().create(float(object[PROP_LABEL_LOCATION].latitude), float(object[PROP_LABEL_LOCATION].longitude))
    elif properties[prop_label] == PROP_VALUE_URL:
        value = py_wb.UrlValue().create(("https://" + object[prop_label]))

    return value

# Update an item in the wikibase
def update_item(py_wb, object):
    item_id = py_wb.Item().getItemId(object[PROP_LABEL_NAME])
    item = py_wb.Item().get(entity_id=item_id)
            
    description = item.description.get()
    
    # check if the descriptions item need to be Updated
    if ITEM_DESCRIPTION in object and object[ITEM_DESCRIPTION] != description:
        item.Description().set(description=object[ITEM_DESCRIPTION])

# create a new item in the wikibase
def create_item(py_wb, object):
    item = py_wb.Item().create(object[PROP_LABEL_NAME])
    
    # Add a description to the item
    if ITEM_DESCRIPTION in object:
        item.Description().set(description=object[ITEM_DESCRIPTION])
        
    return item

# Update the claim with the new value
def update_claim(item, claim, claim_list, prop, value):

    for claim in claim_list[item.entity_id]:
        # Check if the claim value is of type PROP_VALUE_COORDINATE
        if claim.value.__class__.__name__ == PROP_VALUE_COORDINATE:
            if str(claim.value.latitude) != str(value.latitude) or str(claim.value.longitude) != str(value.longitude):
                claim = item.claims.add(prop, value)
                break
            
        # Check if the claim value has changed
        elif str(claim.value).lower() != str(value).lower():
            claim = item.claims.add(prop, value)
            break


# Process items, create or update claims of the items 
def process_item_claims(py_wb, object, properties, claim_list, item, exist_item):
    # Loop through properties and add claims to item
    for prop_label, value in object.items():
        
        # Format property label
        prop_label_formatted = prop_label.replace("_", " ")

        # Get the property id from the Wikibase
        prop_id = py_wb.Property().getPropertyId(prop_label_formatted.capitalize())
        
        # Get the property details from the Wikibase
        prop = py_wb.Property().get(entity_id=prop_id.capitalize())

        # Create value based on data type
        value = create_claim_value(py_wb, properties, prop_label, object)
        
        # If property or value doesn't exist, skip it
        if value == None or prop == None:
            continue
        
        # If item already exists and property is present in the claims, update the claim
        if exist_item and prop_id in claim_list:
            update_claim(item, claim, claim_list, prop, value)
        else:
            # If item doesn't exist or property is not in the claims, add a new claim
            claim = item.claims.add(prop, value)

        # Print details of the statement
        print_statement_details(claim, prop_id, prop_label_formatted)
        
        print()

# Inject the data in the wikibase
def inject_data(py_wb, data, properties):
    # Process properties and create or update properties in the Wikibase
    process_properties(py_wb, properties)
    
    # Loop through data and create Wikibase items with properties and values
    for object in data:
                
        exist_item, claim_list = False, {}
        
        # Check if item already exists in Wikibase
        if py_wb.Item().existItem(object[PROP_LABEL_NAME]):
            # update the item
            item = update_item(py_wb, object)
            exist_item = True
            # Store existing claims of the item
            claim_list = item.claims.to_dict()
        else:
            # create a new item
            item = create_item(py_wb, object)

        # Print details of the item
        print_item(item)

        # Process items, create or update claims of the items 
        process_item_claims(py_wb, object, properties, claim_list, item, exist_item)

        break
        
        # Reset color to default
        print(Style.RESET_ALL)
