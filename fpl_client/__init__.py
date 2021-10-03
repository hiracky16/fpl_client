from fpl_client.repositories.fpl_repository import FPLRepository

class FPLClient:
    def __init__(self):
        self.api = FPLRepository()

    def get_players(self):
        return self.api.get_players()

    def get_teams(self):
        return self.api.get_teams()

    def get_fixtures(self, event=None, team_id=None):
        return self.api.get_fixtures(event=event, team_id=team_id)

    def get_event_live(self, event):
        return self.api.get_event_live(event)
