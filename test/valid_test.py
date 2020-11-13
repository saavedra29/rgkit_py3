import ast
import pkg_resources
import unittest

from rgkit.settings import settings
from rgkit.gamestate import GameState
from rgkit.game import Player

map_data = ast.literal_eval(
    open(pkg_resources.resource_filename('rgkit', 'maps/default.py')).read())
settings.init_map(map_data)


class TestValid(unittest.TestCase):
    def test_ok(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        robot = state.robots[(9, 9)]
        Player._validate_action(robot, ['guard'])
        Player._validate_action(robot, ['suicide'])
        Player._validate_action(robot, ['guard', None])
        Player._validate_action(robot, ['suicide', (1, 1)])
        Player._validate_action(robot, ['attack', (9, 10)])
        Player._validate_action(robot, ['move', (9, 10)])
        Player._validate_action(robot, ('guard', (2, 3)))
        Player._validate_action(robot, ('suicide', None))
        Player._validate_action(robot, ('attack', (9, 10)))
        Player._validate_action(robot, ('move', (9, 10)))

    def test_none(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        robot = state.robots[(9, 9)]
        with self.assertRaises(Exception):
            Player._validate_action(robot, None)

    def test_strange(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        robot = state.robots[(9, 9)]
        with self.assertRaises(Exception):
            Player._validate_action(robot, "ALL YOUR BASE ARE BELONG TO US")

    def test_wrong_command(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        robot = state.robots[(9, 9)]
        with self.assertRaises(Exception):
            Player._validate_action(robot, ['exterminate'])

    def test_lack_of_location(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        robot = state.robots[(9, 9)]

        with self.assertRaises(Exception):
            Player._validate_action(robot, ['move'])

    def test_move_to_self(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        robot = state.robots[(9, 9)]
        with self.assertRaises(Exception):
            Player._validate_action(robot, ['move', (9, 9)])

    def test_move_too_far(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        robot = state.robots[(9, 9)]
        with self.assertRaises(Exception):
            Player._validate_action(robot, ['move', (9, 11)])

    def test_move_to_obstacle(self):
        state = GameState()
        state.add_robot((2, 5), 0)
        robot = state.robots[(2, 5)]
        with self.assertRaises(Exception):
            Player._validate_action(robot, ['move', (2, 4)])

    def test_attack_self(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        robot = state.robots[(9, 9)]
        with self.assertRaises(Exception):
            Player._validate_action(robot, ['attack', (9, 9)])

    def test_attack_too_far(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        robot = state.robots[(9, 9)]
        with self.assertRaises(Exception):
            Player._validate_action(robot, ['attack', (9, 11)])

    def test_attack_obstacle(self):
        state = GameState()
        state.add_robot((2, 5), 0)
        robot = state.robots[(2, 5)]
        with self.assertRaises(Exception):
            Player._validate_action(robot, ['attack', (2, 4)])
