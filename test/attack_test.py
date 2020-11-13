import ast
import pkg_resources
import unittest

from rgkit.settings import settings
from rgkit.gamestate import GameState

map_data = ast.literal_eval(
    open(pkg_resources.resource_filename('rgkit', 'maps/default.py')).read())
settings.init_map(map_data)


class TestAttack(unittest.TestCase):
    def test_attack_does_damage(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)

        actions = {
            (10, 10): ['attack', (9, 10)],
            (9, 10): ['attack', (10, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((10, 10)))
        damage = settings.robot_hp - state2.robots[10, 10].hp
        self.assertTrue(
            settings.attack_range[0] <= damage <= settings.attack_range[1])
        self.assertTrue(state2.is_robot((9, 10)))
        damage = settings.robot_hp - state2.robots[9, 10].hp
        self.assertTrue(
            settings.attack_range[0] <= damage <= settings.attack_range[1])

    def test_attack_kills(self):
        state = GameState()
        state.add_robot((10, 10), 0, hp=settings.attack_range[0])
        state.add_robot((9, 10), 1, hp=settings.attack_range[0])

        actions = {
            (10, 10): ['attack', (9, 10)],
            (9, 10): ['attack', (10, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertFalse(state2.is_robot((10, 10)))
        self.assertFalse(state2.is_robot((9, 10)))

    def test_guarding_reduces_damage(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)

        actions = {
            (10, 10): ['attack', (9, 10)],
            (9, 10): ['guard']
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 10)))
        damage = settings.robot_hp - state2.robots[9, 10].hp
        self.assertTrue(
            settings.attack_range[0]/2 <= damage <= settings.attack_range[1]/2)

    def test_attack_does_no_damage_to_teammates(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 0)

        actions = {
            (10, 10): ['attack', (9, 10)],
            (9, 10): ['attack', (10, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((10, 10)))
        self.assertEqual(state2.robots[10, 10].hp, settings.robot_hp)
        self.assertTrue(state2.is_robot((9, 10)))
        self.assertEqual(state2.robots[9, 10].hp, settings.robot_hp)

    def test_attack_dodge(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)

        actions = {
            (10, 10): ['attack', (9, 10)],
            (9, 10): ['move', (8, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((8, 10)))
        self.assertEqual(state2.robots[8, 10].hp, settings.robot_hp)

    def test_attack_dodge_fail(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)
        state.add_robot((7, 10), 1)

        actions = {
            (10, 10): ['attack', (9, 10)],
            (9, 10): ['move', (8, 10)],
            (7, 10): ['move', (8, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 10)))
        damage = settings.robot_hp - state2.robots[9, 10].hp
        self.assertTrue(
            settings.attack_range[0] <= damage <= settings.attack_range[1])

    def test_attack_hop_in(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((8, 10), 1)

        actions = {
            (10, 10): ['attack', (9, 10)],
            (8, 10): ['move', (9, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 10)))
        damage = settings.robot_hp - state2.robots[9, 10].hp
        self.assertTrue(
            settings.attack_range[0] <= damage <= settings.attack_range[1])
