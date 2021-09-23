from fpl_client.repositories.fpl_api import FPLApi

class FPLClient:
    def __init__(self):
        self.api = FPLApi()

    def get_players(self):
        return self.api.get_players()

    def get_teams(self):
        return self.api.get_teams()
