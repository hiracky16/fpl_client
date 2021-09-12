class Team:
    def __init__(self, obj={}):
        self.id         = obj['id']
        self.name       = obj['name']
        self.short_name = obj['short_name']
        self.draw       = obj['draw']
        self.loss       = obj['loss']
        self.win        = obj['win']

