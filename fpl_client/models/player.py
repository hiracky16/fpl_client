class Player:
    def __init__(self, obj={}):
        self.first_name = obj['first_name']
        self.second_name = obj['second_name']

    def full_name(self):
        return f"{self.first_name} {self.second_name}"

