import os
import requests


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = "EAAagJfZAQMrcBAAmZAXMGAIbvRWEv2VGewoBrWDDwUZBi012N697LV7JYWtA6zSVdlDE7YB5Eo4nAMauQxuH5umYhN6m9j67GyIz3QJt3ur4IQ0HIY011GQd6Hboi7Qxds3CMl5hw3Ad7L192l7YrJaEWGUI0CvwrI08Hx9xAZDZD"


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
