import requests


def write_url(wiki_api_url ,item_id, prop_id, url_value, edit_token):
    # Make the API request to add the URL value to the item
    add_value_url = f"{wiki_api_url}?action=wbcreateclaim&entity={item_id}&property={prop_id}&snaktype=value&value=%7B%22entity-type%22%3A%22url%22%2C%22numeric-id%22%3Anull%2C%22id%22%3A%22{url_value}%22%7D&token={edit_token}"

    response = requests.post(add_value_url)
    print("!=========")
    print(response)
    print("=========!")
