import requests
import urllib.parse


class Location():

    def __init__(self):
        pass

    def get_address(self):
        street = str(input("addresse ? :"))
        city = str(input("ville ? :"))
        cp = str(input("code postal ? :"))
        address = '{},{},{}'.format(street, city, cp)
        return address

    def coordinates(self, address):
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'

        response = requests.get(url).json()
        self.lat = response[0]["lat"]
        self.lng = response[0]["lon"]
        self.coord = {'lat': self.lat, 'lng': self.lng}
        return self.coord

    def run(self):
        return self.coordinates(self.get_address())