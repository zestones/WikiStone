from api_global import session
import json

def write_statement(api_url, edit_token, subjectQNumber, propertyPNumber, value, property_datatype):
    parameters = {
        'action':'wbcreateclaim',
        'format':'json',
        'entity':subjectQNumber,
        'snaktype':'value',
        'bot':'1',  # not sure that this actually does anything
        'token': edit_token,
        'property': propertyPNumber,
        'value': json.dumps(str(value)),
    }
    
    if property_datatype == 'string':
        data_dict = json.dumps(str(value))
    else :
        return
    # elif property_datatype == 'globe-coordinate':
    #     data_dict = json.dumps({"type":"globe-coordinate","latitude":str(value[0]),"longitude":str(value[1]),"precision":"0.000001","globe":"http://www.wikidata.org/entity/Q2"})
   
    parameters['value'] = data_dict 
    print(parameters)
    
    response = session.post(api_url, data=parameters)
    data = response.json()

    if "error" in data:
        print("==== ERROR =====")
        print(response)
        print("----")
        print(data)
        print("----")
        print('-->Failed to add claim for: ' + propertyPNumber)
        print('-->Entity: ' + str(subjectQNumber))
        print('-->Value: ' + str(value))
        print('-->Property data type: ' + property_datatype)
    else:
        print('Added claim for: ' + propertyPNumber)

    return data
