import requests
from .models.player import Player

class FPLClient:
    # fantasy premier league api base url
    BASE_URL = "https://fantasy.premierleague.com/api"

    def __init__(self):
        1 # do something

    def _get(self, path):
        url = f"{self.BASE_URL}/{path}"
        res = requests.get(url)
        return res.json()
    
    def get_players(self):
        path = "bootstrap-static/"
        res = self._get(path)
        elements = res['elements']
        return [Player(e) for e in elements[0:5]]
        
