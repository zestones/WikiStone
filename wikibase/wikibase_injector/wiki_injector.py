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

def inject_data(py_wb, data, properties):
    process_properties(py_wb, properties)
    
    # Loop through data and create Wikibase items with properties and values
    for object in data:
        exist_item, claim_list = False, {}
        
        if py_wb.Item().existItem(object[PROP_LABEL_NAME]):
            item_id = py_wb.Item().getItemId(object[PROP_LABEL_NAME])
            item = py_wb.Item().get(entity_id=item_id)
            
            exist_item = True
            claim_list = item.claims.to_dict()
            
            # TODO : Test Update of description
            description = item.description.get()
            if ITEM_DESCRIPTION in object and object[ITEM_DESCRIPTION] != description:
                item.Description().set(description=object[ITEM_DESCRIPTION])
            
        else : 
            item = py_wb.Item().create(object[PROP_LABEL_NAME])
            # Add a description to the item
            if ITEM_DESCRIPTION in object:
                item.Description().set(description=object[ITEM_DESCRIPTION])

        print(Fore.MAGENTA + "====================== ITEM ======================")
        print(Fore.YELLOW + " |\tItem ID: " + Fore.WHITE +  item.entity_id)
        print(Fore.YELLOW + " |\tItem Label: ", Fore.WHITE,  item.label.get())
        print(Fore.YELLOW + " |\tItem Description: ", Fore.WHITE, item.description.get())

        # Loop through properties and add claims to item
        for prop_label, value in object.items():
            
            prop_label_formatted = prop_label.replace("_", " ")
            print(py_wb.Property().existProperty(prop_label_formatted.capitalize()))
            prop_id = py_wb.Property().getPropertyId(prop_label_formatted.capitalize())
            prop = py_wb.Property().get(entity_id=prop_id.capitalize())

            # Create value based on data type
            value = create_claim_value(py_wb, properties, prop_label, object)
            
            # If property or Value doesn't exist, skip it
            if value == None or prop == None:
                continue
         
            # Update the existant claim
            if exist_item and prop_id in claim_list:
                for claim in claim_list[prop_id]:
                    if claim.value.__class__.__name__ == PROP_VALUE_COORDINATE:
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
            print(Fore.YELLOW + " |\tProperty Label: ", Fore.WHITE, prop_label_formatted)
            print(Fore.YELLOW + " |\tClaim value: " , Fore.WHITE , claim.value)
            
            print()

        print(Style.RESET_ALL)