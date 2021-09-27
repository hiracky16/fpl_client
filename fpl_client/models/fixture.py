class Fixture:
    """試合結果"""
    def __init__(self, obj={}, teams=[]):
        """
        Args:
            obj (dict, optional): [API のレスポンス]. Defaults to {}.
        """
        self.away_team_id = obj['team_a']
        self.home_team_id = obj['team_h']
        self.away_goal = obj['team_a_score']
        self.home_goal = obj['team_h_score']
        self.finished = obj['finished']
        self.event = obj['event']
        self.away_team = list(filter(lambda x: x.id == self.away_team_id, teams))[0]
        self.home_team = list(filter(lambda x: x.id == self.home_team_id, teams))[0]

    def win_team(self):
        """勝利チームの Team オブジェクトを返す
        Returns:
            勝敗が決まっている場合勝利した方の Team オブジェクト
            引き分けの場合 None
            チームオブエジェクトが設定されていない場合例外を起こす
        Raises:
            Exception: home_team と away_team が設定されていない場合
        """
        if not self.home_team or not self.away_team:
            raise Exception('team not set')

        if self.away_goal < self.home_goal:
            return self.home_team
        elif self.home_goal < self.away_goal:
            return self.away_team
        else:
            return None