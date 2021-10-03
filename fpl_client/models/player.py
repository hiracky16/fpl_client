class Player:
    def __init__(self, obj={}):
        attributes = [
            'id',
            'first_name',
            'second_name',
            'total_points',
            'points_per_game',
            'minutes'
        ]
        for a in attributes:
            exec(f"self.{a} = obj['{a}']")
        self.image_url = f'https://resources.premierleague.com/premierleague/photos/players/250x250/p{obj["photo"]}'

    def full_name(self):
        return f"{self.first_name} {self.second_name}"

