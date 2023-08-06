import json
import requests
from os import path

REQ_SAVE_FILE_NAME = path.realpath(__file__).replace("__init__.py", "place_address_to_google_places.json")

class SearchAddressGoogleAPI():
    def __init__(self, key):
        self.key = key
        if not path.exists(REQ_SAVE_FILE_NAME):
            self.previous_search_request = {}
            self.update_file_data()

        with open(REQ_SAVE_FILE_NAME) as f:
            self.previous_search_request = json.load(f)

    def update_file_data(self):
        with open(REQ_SAVE_FILE_NAME, 'w') as outfile:
            json.dump(self.previous_search_request, outfile, indent=2)

    def update_search_request(self, search_key, search_google_places_obj):
        self.previous_search_request[search_key] = search_google_places_obj
        self.update_file_data()

    def search_google(self, addr):
        if not self.key:
            raise Exception("Google API Key is not found")

        formatted_addr = addr.replace(", ", "+").replace(",", "+")
        if formatted_addr not in self.previous_search_request:
            resp = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(
                    formatted_addr, self.key))
            if (resp.json()["status"] == "REQUEST_DENIED"):
                return resp.json()
            else:
                self.previous_search_request[formatted_addr] = resp.json()
                self.update_file_data()
                print("Made Google Request")

        return self.previous_search_request[formatted_addr]