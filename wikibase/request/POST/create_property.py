import sys
sys.path.append('../')
import api_global

# create a new property
# property : label for the new property
# data type of the new property, can be "string", "wikibase-item", "time", etc.
def create_property(api_url, edit_token, property_label, property_datatype):
    parameters = {
        'action': 'wbeditentity',
        'format': 'json',
        'new': 'property',
        'token': edit_token,
        'data': '{"labels":{"en":{"language":"en","value":"' + property_label + '"}},"datatype":"' + property_datatype + '"}'
    }

    r = api_global.session.post(api_url, data=parameters)
    data = r.json()
    
    return data