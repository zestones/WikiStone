from wikibase_injector.data_formatter.label_properties import *
from colorama import Fore, Style


# Print the details of an item
def print_item(item):
    print(Fore.MAGENTA + "=" * 11 + " ITEM " + 11 * "=")
    print(Fore.YELLOW + " |\tItem ID: " + Fore.WHITE + item.entity_id)
    print(Fore.YELLOW + " |\tItem Label: ", Fore.WHITE,  item.label.get())
    print(Fore.YELLOW + " |\tItem Description: ",
          Fore.WHITE, item.description.get())
    print()


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
