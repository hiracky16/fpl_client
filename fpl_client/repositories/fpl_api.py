from fpl_client.models.fixture import Fixture
from fpl_client.models.player import Player
from fpl_client.models.team import Team
import requests, datetime, json, os
from os.path import join, dirname

class FPLApi:
    # fantasy premier league api base url
    BASE_URL = "https://fantasy.premierleague.com/api"

    # number of days for saving cache.
    THRESHHOLD_DAYS = 7

    def _generate_file_path(self, filename):
        current_dir = dirname(__file__)
        # NOTE: fpl_client/data/ 配下にするためのややこしい処理
        data_dir = '/'.join(current_dir.split('/')[:-1]) + '/data'
        return join(data_dir, filename)

    def _is_valid_cache(self, path):
        cache_date_file = self._generate_file_path(f"{path}.timestamp")
        if not os.path.exists(cache_date_file):
            return False

        cache_file = self._generate_file_path(f"{path}.json")
        if not os.path.exists(cache_file):
            return False

        with open(cache_date_file) as f:
            data = f.read()
            saved_date = datetime.datetime.strptime(data, '%Y-%m-%d')
            diff = datetime.date.today() - saved_date.date()
            return diff.days < self.THRESHHOLD_DAYS

    def _read_cache_file(self, path):
        with open(self._generate_file_path(f"{path}.json")) as f:
            return json.load(f)

    def _write_cache_file(self, path, data):
        with open(self._generate_file_path(f"{path}.json"), 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with open(self._generate_file_path(f"{path}.timestamp"), 'w') as f:
            f.write(f'{datetime.date.today()}')

    def _get(self, path):
        if self._is_valid_cache(path):
            return self._read_cache_file(path)
        else:
            url = f"{self.BASE_URL}/{path}"
            if '?' in url:
                url = url + '/'
            res = requests.get(url)
            data = res.json()
            self._write_cache_file(path, data)
            return data

    def get_players(self):
        path = "bootstrap-static"
        res = self._get(path)
        elements = res['elements']
        return [Player(e) for e in elements]

    def get_teams(self):
        path = "bootstrap-static"
        res = self._get(path)
        teams = res['teams']
        return [Team(t) for t in teams]

    def get_fixtures(self, event=None):
        path = f'fixtures?event={event}' if event else 'fixtures'
        res = self._get(path)
        teams = self.get_teams()
        fixtures = []
        for r in res:
            fixture = Fixture(r)
            fixture.set_team(teams)
            fixtures.append(fixture)
        return fixtures