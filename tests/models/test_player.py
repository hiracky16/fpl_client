import sys, unittest
sys.path.append('../../')
from fpl_client.models.player import Player

class TestPlayer(unittest.TestCase):
    TEST_PLAYER_OBJECT = {
        'first_name': 'George',
        'second_name': 'Best'
    }

    def setUp(self):
        self.player = Player(self.TEST_PLAYER_OBJECT)

    def test_full_name(self):
        self.assertEqual(self.player.full_name(), f"{self.TEST_PLAYER_OBJECT['first_name']} {self.TEST_PLAYER_OBJECT['second_name']}")

if __name__ == "__main__":
    unittest.main()
