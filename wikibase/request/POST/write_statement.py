import api_global

# pass in the local names including the initial letter as strings, e.g. ('Q3345', 'P6', 'Q1917')
# ! the property should exist otherwise the statement will not be created
def writeStatement(api_url, edit_token, subjectQNumber, propertyPNumber, objectQNumber):

    strippedQNumber = objectQNumber[1:len(objectQNumber)] # remove initial "Q" from object string

    parameters = {
        'action':'wbcreateclaim',
        'format':'json',
        'entity':subjectQNumber,
        'snaktype':'value',
        'bot':'1',  # not sure that this actually does anything
        'token': edit_token,
        'property': propertyPNumber,
        # note: the value is a string, not an actual data structure.  I think it will get URL encoded by requests before posting
        'value':'{"entity-type":"item","numeric-id":' + strippedQNumber+ '}'
    }
    r = api_global.session.post(api_url, data=parameters)
    data = r.json()
    
    return data
