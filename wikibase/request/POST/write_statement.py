from api_global import session

# pass in the local names including the initial letter as strings, e.g. ('Q3345', 'P6', 'Q1917')
# ! the property should exist otherwise the statement will not be created
def write_statement(api_url, edit_token, subjectQNumber, propertyPNumber, value, property_datatype):

    parameters = {
        'action':'wbcreateclaim',
        'format':'json',
        'entity':subjectQNumber,
        'bot':'1',  # not sure that this actually does anything
        'token': edit_token,
        'property': propertyPNumber,
    }

    if property_datatype == "wikibase-item":
        strippedQNumber = value[1:len(value)] # remove initial "Q" from object string
        parameters['snaktype'] = 'value'
        parameters['value'] = '{"entity-type":"item","numeric-id":' + strippedQNumber + '}'
    elif property_datatype == "string":
        parameters['snaktype'] = 'value'
        parameters['value'] = '{"type":"string","value":"' + value + '"}'
    elif property_datatype == "time":
        parameters['snaktype'] = 'value'
        parameters['value'] = '{"type":"time","time":"' + value + '","calendarmodel":"http://www.wikidata.org/entity/Q1985727"}'
    elif property_datatype == "globe-coordinate":
        parameters['snaktype'] = 'value'
        parameters['value'] = '{"type":"globe-coordinate","latitude":' + str(value[0]) + ',"longitude":' + str(value[1]) + ',"precision":0.000001,"globe":"http://www.wikidata.org/entity/Q2"}'
    else:
        print("Invalid datatype: " + str(property_datatype))
        return

    response = session.post(api_url, data=parameters)
    data = response.json()

    if "success" in response and response["success"] == 1:
        print('Added claim for: ' + propertyPNumber)
    else:
        print(response)
        print('Failed to add claim for: ' + propertyPNumber)
        print('Entity: ' + str(subjectQNumber))

    return data
