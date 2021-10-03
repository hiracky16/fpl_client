from fpl_client.models.fixture import Fixture
from fpl_client.models.player import Player
from fpl_client.models.team import Team
from fpl_client.models.event_element import EventElement
import requests, datetime, json, os
from os.path import join, dirname

class FPLRepository:
    """FPL API へリクエストしたり結果をキャッシュしたりする
    """
    # fantasy premier league api base url
    BASE_URL = "https://fantasy.premierleague.com/api"

    # number of days for saving cache.
    THRESHHOLD_DAYS = 7

    def _generate_file_path(self, filename):
        """キャッシュファイルのディレクトリ
        Args:
            filename ([String]): [キャッシュファイル]
        Returns:
            [String]: [キャッシュファイルのパス]
        """
        current_dir = dirname(__file__)
        # NOTE: fpl_client/data/ 配下にするためのややこしい処理
        data_dir = '/'.join(current_dir.split('/')[:-1]) + '/data'
        return join(data_dir, filename)

    def _is_valid_cache(self, path):
        """キャッシュが有効かチェックするメソッド
        API のキャッシュは 7 日間有効
        Args:
            path ([String]): [API のパス]
        Returns:
            [Boolean]: [キャッシュの有効か]
        """
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
        """API にリクエストせずキャッシュを読む
        Args:
            path ([String]): [API のパス]
        Returns:
            [dict]: [API のレスポンス]
        """
        with open(self._generate_file_path(f"{path}.json")) as f:
            return json.load(f)

    def _write_cache_file(self, path, data):
        """API のレスポンスをキャッシュするためのメソッド
        Args:
            path ([type]): [API のパス]
            data ([dict]): [キャッシュする API のレスポンス]
        """
        file_name = path.replace("/", "_")
        with open(self._generate_file_path(f"{file_name}.json"), 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with open(self._generate_file_path(f"{file_name}.timestamp"), 'w') as f:
            f.write(f'{datetime.date.today()}')

    def _get(self, path):
        """Fantasy Premier League API への HTTP リクエスト
        Args:
            path ([String ]): [API のパス]
        Returns:
            [dict]: [API のレスポンスを dict 型に変換したもの]
        """
        if self._is_valid_cache(path):
            return self._read_cache_file(path)
        else:
            url = f"{self.BASE_URL}/{path}"
            if '?' not in url:
                url = url + '/'
            res = requests.get(url)
            data = res.json()
            if len(data.keys()) == 0:
                raise "no keys"

            self._write_cache_file(path, data)
            return data

    def get_players(self):
        """選手一覧を返す
        Returns:
            players [Player]: [選手一覧]
        """
        path = "bootstrap-static"
        res = self._get(path)
        elements = res['elements']
        return [Player(e) for e in elements]

    def get_teams(self):
        """チーム一覧を取得
        Returns:
            teams [Team]: [チーム一覧]
        """
        path = "bootstrap-static"
        res = self._get(path)
        teams = res['teams']
        return [Team(t) for t in teams]

    def get_fixtures(self, event=None, team_id=None):
        """試合結果を返すメソッド
        Args:
            event ([type], optional): [第何節目か]. Defaults to None.
            team_id ([type], optional): [チームを限定する]. Defaults to None.
        Returns:
            fixtures [Fixture]: [結果一覧]
        """
        path = f'fixtures?event={event}' if event else 'fixtures'
        res = self._get(path)
        teams = self.get_teams()
        fixtures = []
        for r in res:
            fixture = Fixture(obj=r, teams=teams)
            if team_id and \
                (fixture.away_team_id != team_id and fixture.home_team_id != team_id):
                continue
            fixtures.append(fixture)
        return fixtures


    def get_event_live(self, event):
        """節ごとの選手のパフォーマンスを返す

        Args:
            event [Integer]: 第 n 節
        """
        path = f'event/{event}/live'
        res = self._get(path)
        elements = res['elements']
        return [EventElement(e) for e in elements]