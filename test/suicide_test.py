

import ast
import pkg_resources
import unittest

from rgkit.settings import settings
from rgkit.gamestate import GameState

map_data = ast.literal_eval(
    open(pkg_resources.resource_filename('rgkit', 'maps/default.py')).read())
settings.init_map(map_data)


class TestSuicide(unittest.TestCase):
    def test_basic_suicide(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)

        actions = {
            (10, 10): ['attack', (9, 10)],
            (9, 10): ['suicide']
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((10, 10)))
        self.assertEqual(state2.robots[10, 10].hp,
                         settings.robot_hp - settings.suicide_damage)

        self.assertFalse(state2.is_robot((9, 10)))

    def test_guarding_reduces_damage(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)

        actions = {
            (10, 10): ['guard'],
            (9, 10): ['suicide']
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((10, 10)))
        self.assertEqual(state2.robots[10, 10].hp,
                         settings.robot_hp - settings.suicide_damage//2)
        self.assertFalse(state2.is_robot((9, 10)))

    def test_suicide_does_no_damage_to_teammates(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 0)

        actions = {
            (10, 10): ['guard'],
            (9, 10): ['suicide']
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((10, 10)))
        self.assertEqual(state2.robots[10, 10].hp, settings.robot_hp)
        self.assertFalse(state2.is_robot((9, 10)))

    def test_suicide_dodge(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)

        actions = {
            (10, 10): ['sucide'],
            (9, 10): ['move', (8, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((8, 10)))
        self.assertEqual(state2.robots[8, 10].hp, settings.robot_hp)

    def test_suicide_dodge_fail(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)
        state.add_robot((7, 10), 1)

        actions = {
            (10, 10): ['suicide'],
            (9, 10): ['move', (8, 10)],
            (7, 10): ['move', (8, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 10)))
        self.assertEqual(state2.robots[9, 10].hp,
                         settings.robot_hp - settings.suicide_damage)

    def test_move_into_suicide_bot(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)

        actions = {
            (10, 10): ['suicide'],
            (9, 10): ['move', (10, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 10)))
        self.assertEqual(state2.robots[9, 10].hp,
                         settings.robot_hp -
                         settings.collision_damage -
                         settings.suicide_damage)
