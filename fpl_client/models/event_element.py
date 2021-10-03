class EventElement:
    """ api/event/{event}/live/ のレスポンス中の element
        => 各節ごとの選手のパフォーマンス
    """
    def __init__(self, obj={}):
        self.id = obj['id']
        self.minutes = obj['stats']['minutes']
        self.total_points = obj['stats']['total_points']
