import requests
import api_global

# where the bot username is after the equals sign on the first line and the bot password
# is after the equals sign on the second line. Make sure there are no extraneous spaces,
# no trailing slash after the URL, and that the lines are in this exact order.
# It doesn't matter whether there is a trailing newline or not.
def retrieve_credentials():
    with open('credentials.txt', 'rt') as file_object:
        lineList = file_object.read().split('\n')
    
    endpoint_url = lineList[0].split('=')[1]
    username = lineList[1].split('=')[1]
    password = lineList[2].split('=')[1]
    
    credentials = [endpoint_url, username, password]
    return credentials

# The loginToken is a random generated string associated with the session
def get_login_token(apiUrl):    
    parameters = {
        'action':'query',
        'meta':'tokens',
        'type':'login',
        'format':'json'
    }

    r = api_global.session.get(url=apiUrl, params=parameters)
    data = r.json()
    
    return data['query']['tokens']['logintoken']

# The result of this function is a successful session login.  
# The response looks like this:
# {'login': {'result': 'Success', 'lguserid': 4, 'lgusername': 'Baskauf'}}
def logIn(apiUrl, token, username, password):
    parameters = {
        'action':'login',
        'lgname':username,
        'lgpassword':password,
        'lgtoken':token,
        'format':'json'
    }

    r = api_global.session.post(apiUrl, data=parameters)
    data = r.json()
    
    # This information isn't actually needed for anything - it's just an indication of a successful session login
    return data

# The CSRF (edit) token is an edit token that is actually used to authorize particular write actions
# It is used to prevent cross-site request forgery (csrf) attacks. I think it's primarily relevant when web forms are used
# Here's the page that shows how to get an edit token
# https://www.mediawiki.org/wiki/API:Edit
def get_csrf_token(apiUrl): # nothing gets passed in because the session instance is already authenticated
    parameters = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    r = api_global.session.get(url=apiUrl, params=parameters)
    data = r.json()
    # The response looks like this:
    # {'batchcomplete': '', 'query': {'tokens': {'csrftoken': '6bc490bb0d2e78cb3f8a2b94e8159da85cdc2484+\\'}}}
    return data["query"]["tokens"]["csrftoken"]


def authenticate():
    print('-------------- AUTHENTIFICATION ----------------')

    credentials = retrieve_credentials()
    print('Credentials: ', credentials)
    print()
    url = credentials[0] + api_global.resourceUrl
    user = credentials[1]
    pwd = credentials[2]

    loginToken = get_login_token(url)
    print('Login token: ',loginToken)
    print()

    data = logIn(url, loginToken, user, pwd)
    print('Confirm login: ', data)
    print()

    csrfToken = get_csrf_token(url)
    print('CSRF token: ', csrfToken)
    print()
    print('----------------------------------------------')
