
import json
import api_global

# the data passed to the API must be JSON in string form.  Because of Python's use of curly braces in format strings, it's
# best to create the data to be passed as a dictionary, then use json.dumps to convert it into string form. 
# Here's what we are building:
'''
dataDict = {
    "labels":{
        "en":{"language":"en","value":"Fred Pig"},
        "es":{"language":"es","value":"Puerco Frederico"}
        },
    "descriptions":{
        "en":{"language":"en","value":"a fake superhero character"}
        }
    }
'''
def createEntity(api_url, edit_token, list_of_labels, list_of_descriptions):

    dataDict, innerDict = {}, {}
    for label in list_of_labels:
        innerDict[label['language']] = {"language": label['language'], "value": label['string']}
   
    dataDict['labels'] =  innerDict

    innerDict = {}
    for description in list_of_descriptions:
        innerDict[description['language']] = {"language": description['language'], "value": description['string']}
    
    dataDict['descriptions'] =  innerDict

    dataString = json.dumps(dataDict)
    parameters = {
        'action': 'wbeditentity',
        'format': 'json',
        'new': 'item',
        'token': edit_token,
        # note: the data value is a string.  I think it will get URL encoded by requests before posting
        'data': dataString
    }
    r = api_global.session.post(api_url, data=parameters)
    response = r.text
    if response[2:7] == 'error':
        print(r.response)
        return "error"
    else:
        data = r.json()
        return data["entity"]["id"]
