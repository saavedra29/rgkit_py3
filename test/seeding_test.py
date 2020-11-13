import ast
import pkg_resources
import unittest

from rgkit.settings import settings
from rgkit import game

map_data = ast.literal_eval(
    open(pkg_resources.resource_filename('rgkit', 'maps/default.py')).read())
settings.init_map(map_data)


class TestSeeding(unittest.TestCase):
    def test_seeding_saves_spawning(self):
        seed = 42
        file1 = pkg_resources.resource_filename(
            'rgkit', 'bots/guardbot.py')
        file2 = pkg_resources.resource_filename(
            'rgkit', 'bots/guardbot.py')

        player1 = game.Player(file1)
        player2 = game.Player(file2)
        game1 = game.Game([player1, player2],
                          print_info=False,
                          record_actions=False,
                          record_history=True,
                          seed=seed)

        game1.run_all_turns()

        player1 = game.Player(file1)
        player2 = game.Player(file2)
        game2 = game.Game([player1, player2],
                          print_info=False,
                          record_actions=True,
                          record_history=True,
                          seed=seed)

        game2.run_all_turns()

        self.assertEqual(game1.history, game2.history)

    def test_seeding_saves_random(self):
        seed = 42
        file1 = pkg_resources.resource_filename(
            'rgkit', 'bots/randombot.py')
        file2 = pkg_resources.resource_filename(
            'rgkit', 'bots/randombot.py')

        player1 = game.Player(file1)
        player2 = game.Player(file2)
        game1 = game.Game([player1, player2],
                          print_info=False,
                          record_actions=False,
                          record_history=True,
                          seed=seed)

        game1.run_all_turns()

        player1 = game.Player(file1)
        player2 = game.Player(file2)
        game2 = game.Game([player1, player2],
                          print_info=False,
                          record_actions=True,
                          record_history=True,
                          seed=seed)

        game2.run_all_turns()

        self.assertEqual(game1.history, game2.history)
