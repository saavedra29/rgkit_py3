import ast
import pkg_resources
import unittest

from rgkit.gamestate import GameState
from rgkit.settings import settings

map_data = ast.literal_eval(
    open(pkg_resources.resource_filename('rgkit', 'maps/default.py')).read())
settings.init_map(map_data)


class TestStateMisc(unittest.TestCase):
    def test_add_robot(self):
        state = GameState()
        state.add_robot((9, 9), 0, robot_id=7, hp=42)
        self.assertTrue((9, 9) in state.robots)
        self.assertEqual(state.robots[(9, 9)].player_id, 0)
        self.assertEqual(state.robots[(9, 9)].robot_id, 7)
        self.assertEqual(state.robots[(9, 9)].hp, 42)

    def test_robot_ids_are_unique(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        state.add_robot((8, 8), 0)
        self.assertNotEqual(state.robots[(9, 9)].robot_id,
                             state.robots[(8, 8)].robot_id)

    def test_is_robot(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        self.assertTrue(state.is_robot((9, 9)))
        self.assertFalse(state.is_robot((8, 8)))

    def test_remove_robot(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        state.remove_robot((9, 9))
        self.assertFalse(state.is_robot((9, 9)))

    def test_scores(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        state.add_robot((6, 11), 1)
        state.add_robot((8, 14), 0)
        self.assertEqual(state.get_scores(), [2, 1])

    def test_get_game_info(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        state.add_robot((6, 11), 1)
        game_info = state.get_game_info(0)
        self.assertEqual(game_info.robots[9, 9].location, (9, 9))
        self.assertEqual(game_info.robots[9, 9].hp, state.robots[(9, 9)].hp)
        self.assertEqual(game_info.robots[9, 9].player_id,
                          state.robots[(9, 9)].player_id)
        self.assertEqual(game_info.robots[9, 9].robot_id,
                          state.robots[(9, 9)].robot_id)
        self.assertEqual(game_info.robots[6, 11].location, (6, 11))
        self.assertEqual(game_info.robots[6, 11].hp, state.robots[(6, 11)].hp)
        self.assertEqual(game_info.robots[6, 11].player_id,
                          state.robots[(6, 11)].player_id)
        self.assertRaises(AttributeError,
                          lambda: game_info.robots[6, 11].robot_id)
        self.assertEqual(game_info.turn, state.turn)
