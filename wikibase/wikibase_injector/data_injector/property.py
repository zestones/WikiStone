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
        if updated:
            print_property(prop, "UPDATED PROPERTY")
        else:
            print_property(prop, "FOUND PROPERTY")


# Create the properties if they don't exist
def process_properties(py_wb, properties):
    print(Fore.GREEN + "*" * 45)
    print(">{:^45}".format(Fore.BLUE + "PROCESS PROPERTIES"))
    print(Fore.GREEN + "*" * 45 + Style.RESET_ALL)

    for property in properties.values():
        prop_label_formatted = property[LABEL].replace("_", " ")

        create_property(py_wb, prop_label_formatted.capitalize(), property)
