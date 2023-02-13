from wikibase_injector.data_formatter.label_properties import *
from colorama import Fore, Style


# Print the details of a property
def print_property(prop, title):
    print(Fore.YELLOW + "_________________________________________")
    print(Fore.BLUE + "|========================================|")
    print(Fore.BLUE + "| " + " " * 12 + " " + Fore.MAGENTA + title + " ")
    print(Fore.BLUE + "|" + "=" * 40 + "|")
    print(Fore.CYAN + "| Property Id : " + Fore.WHITE + str(prop.entity_id))
    print(Fore.CYAN + "| Label: " + Fore.WHITE + str(prop.label))
    print(Fore.CYAN + "| Data Type : " + Fore.WHITE + str(prop.data_type))
    print(Fore.CYAN + "| Description: " + Fore.WHITE + str(prop.description))
    print(Fore.YELLOW + "------------------------------------------" + Style.RESET_ALL)


# Print the details of an item
def print_item(item):
    print(Fore.MAGENTA + "=" *11 + " ITEM " + 11 * "=")
    print(Fore.YELLOW + " |\tItem ID: " + Fore.WHITE + item.entity_id)
    print(Fore.YELLOW + " |\tItem Label: ", Fore.WHITE,  item.label.get())
    print(Fore.YELLOW + " |\tItem Description: ",
          Fore.WHITE, item.description.get())
    print()

# Print the details of a statement
def print_statement_details(claim, prop_id, prop_label):
    print("---------- " + Fore.BLUE + "Statements" + Fore.WHITE + " ----------")
    print(Fore.YELLOW + " |\tClaim rank: ", Fore.WHITE, claim.rank)

    print("............ " + Fore.BLUE + "Property" + Fore.WHITE + " ............")
    print(Fore.YELLOW + " |\tProperty ID: ", Fore.WHITE, prop_id)
    print(Fore.YELLOW + " |\tProperty Label: ", Fore.WHITE, prop_label)
    print(Fore.YELLOW + " |\tClaim value: ", Fore.WHITE, claim.value)


# Update property
def update_property(py_wb, prop, prop_label, property):
    updated = False
    
    # Update the property description if it has changed
    if str(prop.description.get()) != property[DESCRIPTION]:
        prop.description.set(property[DESCRIPTION], language=py_wb.language)
        updated = True
        
    # Update the property label if it has changed
    if prop_label != property[LABEL].capitalize():
        prop.label.set(prop_label, language=py_wb.language)
        updated = True

    return updated


# Define function to create properties if they don't exist
def create_property(py_wb, prop_label, property):
    if not py_wb.Property().existProperty(prop_label):
        prop = py_wb.Property().create(prop_label, data_type=property[TYPE])
        print_property(prop, "NEW PROPERTY")
    else:
        prop_id = py_wb.Property().getPropertyId(prop_label)
        prop = py_wb.Property().get(entity_id=prop_id)

        updated = update_property(py_wb, prop, prop_label, property)
        
        # Print property details
        if updated: print_property(prop, "UPDATED PROPERTY")
        else: print_property(prop, "FOUND PROPERTY")
        

# Create the properties if they don't exist
def process_properties(py_wb, properties):
    print(Fore.GREEN + "*" * 45)
    print(">{:^45}".format(Fore.BLUE + "PROCESS PROPERTIES"))
    print(Fore.GREEN + "*" * 45 + Style.RESET_ALL)
    
    for property in properties.values():
        prop_label_formatted = property[LABEL].replace("_", " ")

        create_property(py_wb, prop_label_formatted.capitalize(), property)


# Create the value for the claim
def create_claim_value(py_wb, properties, prop_label, object):
    value = None

    # Check that the prop SHOULD be added to the claim
    # ! The DESCRIPTION is a label of the item not the claim
    if prop_label not in properties:
        return value
    
    # TODO : Declare type in other FILE
    if properties[prop_label][TYPE] == TYPE_STRING:
        value = py_wb.StringValue().create(object[prop_label])
    elif properties[prop_label][TYPE] == "monolingualtext":
        value = py_wb.MonolingualTextValue().create(
            object[prop_label], language="fr")
    elif properties[prop_label][TYPE] == "quantity":
        value = py_wb.Quantity().create(object[prop_label])
    elif properties[prop_label][TYPE] == "wikibase-item":
        value = py_wb.Item().get(entity_id=object[prop_label])
    elif properties[prop_label][TYPE] == TYPE_COORDINATE:
        value = py_wb.GeoLocation().create(
            float(object[prop_label][0]), float(object[prop_label][1]))
    elif properties[prop_label][TYPE] == TYPE_URL:
        value = py_wb.UrlValue().create(("https://" + object[prop_label]))

    return value


# Update an item in the wikibase
def update_item(py_wb, object):
    item_id = py_wb.Item().getItemId(object[PROP_NAME[LABEL]])
    item = py_wb.Item().get(entity_id=item_id)

    description = item.description.get()

    # check if the descriptions item need to be Updated
    if ITEM_DESCRIPTION in object and object[ITEM_DESCRIPTION] != description:
        item.description.set(description=object[ITEM_DESCRIPTION])

    return item


# create a new item in the wikibase
def create_item(py_wb, object):
    item = py_wb.Item().create(object[PROP_NAME[LABEL]])

    # Add a description to the item
    if ITEM_DESCRIPTION in object:
        item.description.set(description=object[ITEM_DESCRIPTION])

    return item


# Update the claim with the new value
def update_claim(item, claim_list, prop, value):
    update_claim = []

    for claim in claim_list[prop.entity_id]:
        # Check if the claim value is of type TYPE_COORDINATE
        if claim.value.__class__.__name__ == TYPE_COORDINATE:
            if str(claim.value.latitude) != str(value.latitude) or str(claim.value.longitude) != str(value.longitude):
                update_claim.append(item.claims.add(prop, value))

        # Check if the claim value has changed
        elif str(claim.value).lower() != str(value).lower():
            update_claim.append(item.claims.add(prop, value))

        return update_claim


# Process items, create or update claims of the items
def process_item_claims(py_wb, object, properties, claim_list, item, exist_item):
    # Loop through properties and add claims to item
    for obj_label, value in object.items():

        # Format property label
        obj_label_formatted = obj_label.replace("_", " ")

        # Get the property id from the Wikibase
        prop_id = py_wb.Property().getPropertyId(obj_label_formatted.capitalize())

        # Get the property details from the Wikibase
        prop = py_wb.Property().get(entity_id=prop_id.capitalize())

        # Create value based on data type
        value = create_claim_value(py_wb, properties, obj_label, object)

        # If property or value doesn't exist, skip it
        if value == None or prop == None:
            continue

        # If item already exists and property is present in the claims, update the claim
        if exist_item and prop_id in claim_list:
            need_update = update_claim(item, claim_list, prop, value)
            # Print updated claim
            print(Fore.BLUE + "=" * 5, Fore.GREEN, len(need_update),
                  "UPDATED CLAIM " + Fore.BLUE + 5 * "=")
            _ = [print_statement_details(
                claim, prop_id, obj_label_formatted) for claim in need_update]
        else:
            # If item doesn't exist or property is not in the claims, add a new claim
            claim = item.claims.add(prop, value)

            # Print details of the statement
            print_statement_details(claim, prop_id, obj_label_formatted)

        print()

# Process entities and create/update entity/claim/statement
def process_entities(py_wb, data, properties):
    print(Fore.GREEN + "*" * 45)
    print(">{:^45}".format(Fore.BLUE + "PROCESS ENTITIES"))
    print(Fore.GREEN + "*" * 45 + Style.RESET_ALL)
    
    # Loop through data and create Wikibase items with properties and values
    for object in data:

        exist_item, claim_list = False, {}
        item = None

        # Check if item already exists in Wikibase
        if py_wb.Item().existItem(object[PROP_NAME[LABEL]]):
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
        process_item_claims(py_wb, object, properties,
                            claim_list, item, exist_item)

        # Reset color to default
        print(Style.RESET_ALL)


# Inject the data in the wikibase
def inject_data(py_wb, data, properties):
    # Process properties and create or update properties in the Wikibase
    process_properties(py_wb, properties)
    
    print()
    
    # Process entities and create/update entity/claim/statement in the Wikibase
    process_entities(py_wb, data, properties)
