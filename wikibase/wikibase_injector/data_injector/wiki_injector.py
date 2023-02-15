from wikibase_injector.data_formatter.label_properties import *
from colorama import Fore, Style
from wikibase_injector.data_injector.property import process_properties
from wikibase_injector.data_injector.claim import process_item_claims
from wikibase_injector.data_injector.item import *


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
