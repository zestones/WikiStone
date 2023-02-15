from wikibase_injector.data_formatter.label_properties import *
from colorama import Fore


# Print the details of a statement
def print_statement_details(claim, prop_id, prop_label):
    print("---------- " + Fore.BLUE + "Statements" + Fore.WHITE + " ----------")
    print(Fore.YELLOW + " |\tClaim rank: ", Fore.WHITE, claim.rank)

    print("............ " + Fore.BLUE +
          "Property" + Fore.WHITE + " ............")
    print(Fore.YELLOW + " |\tProperty ID: ", Fore.WHITE, prop_id)
    print(Fore.YELLOW + " |\tProperty Label: ", Fore.WHITE, prop_label)
    print(Fore.YELLOW + " |\tClaim value: ", Fore.WHITE, claim.value)


# ! ######### CLAIMS #########
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
