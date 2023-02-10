
import json
from api_global import session

# the data passed to the API must be JSON in string form.  Because of Python's use of curly braces in format strings, it's
# best to create the data to be passed as a dictionary, then use json.dumps to convert it into string form. 
# Here's what we are building:
'''
data_dict = {
    "labels":{
        "en":{"language":"en","value":"Fred Pig"},
        "es":{"language":"es","value":"Puerco Frederico"}
        },
    "descriptions":{
        "en":{"language":"en","value":"a fake superhero character"}
        }
    }
'''
def create_entity(api_url, edit_token, list_of_labels, list_of_descriptions):

    data_dict, inner_dict = {}, {}
    for label in list_of_labels:
        inner_dict[label['language']] = {"language": label['language'], "value": label['string']}
   
    data_dict['labels'] =  inner_dict

    inner_dict = {}
    for description in list_of_descriptions:
        inner_dict[description['language']] = {"language": description['language'], "value": description['string']}
    
    data_dict['descriptions'] =  inner_dict

    data_string = json.dumps(data_dict)
    parameters = {
        'action': 'wbeditentity',
        'format': 'json',
        'new': 'item',
        'token': edit_token,
        # note: the data value is a string.  I think it will get URL encoded by requests before posting
        'data': data_string
    }
    
    r = session.post(api_url, data=parameters)
    response = r.text
    
    if response[2:7] == 'error':
        # print(response)
        return "error"
    else:
        data = r.json()
        return data["entity"]["id"]
