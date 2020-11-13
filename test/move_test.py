import ast
import pkg_resources
import unittest

from rgkit.settings import settings
from rgkit.gamestate import GameState

map_data = ast.literal_eval(
    open(pkg_resources.resource_filename('rgkit', 'maps/default.py')).read())
settings.init_map(map_data)


class TestMove(unittest.TestCase):
    def test_move_no_collision(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((8, 10), 0)

        actions = {
            (10, 10): ['move', (11, 10)],
            (8, 10): ['move', (7, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((11, 10)))
        self.assertEqual(state2.robots[11, 10].hp, settings.robot_hp)
        self.assertTrue(state2.is_robot((7, 10)))
        self.assertEqual(state2.robots[7, 10].hp, settings.robot_hp)

    def test_basic_collision(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((8, 10), 1)

        actions = {
            (10, 10): ['move', (9, 10)],
            (8, 10): ['move', (9, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((10, 10)))
        self.assertEqual(state2.robots[10, 10].hp,
                         settings.robot_hp - settings.collision_damage)
        self.assertTrue(state2.is_robot((8, 10)))
        self.assertEqual(state2.robots[8, 10].hp,
                         settings.robot_hp - settings.collision_damage)

    def test_guarding_ingnores_collisions(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((9, 10), 1)

        actions = {
            (10, 10): ['move', (9, 10)],
            (9, 10): ['guard']
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((10, 10)))
        self.assertEqual(state2.robots[10, 10].hp,
                         settings.robot_hp - settings.collision_damage)
        self.assertTrue(state2.is_robot((9, 10)))
        self.assertEqual(state2.robots[9, 10].hp, settings.robot_hp)

    def test_move_train(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((11, 10), 0)
        state.add_robot((12, 10), 0)

        actions = {
            (10, 10): ['move', (9, 10)],
            (11, 10): ['move', (10, 10)],
            (12, 10): ['move', (11, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 10)))
        self.assertEqual(state2.robots[9, 10].hp, settings.robot_hp)
        self.assertTrue(state2.is_robot((10, 10)))
        self.assertEqual(state2.robots[10, 10].hp, settings.robot_hp)
        self.assertTrue(state2.is_robot((11, 10)))
        self.assertEqual(state2.robots[11, 10].hp, settings.robot_hp)

    def test_train_collision(self):
        state = GameState()
        state.add_robot((10, 10), 0)
        state.add_robot((11, 10), 1)
        state.add_robot((12, 10), 0)
        state.add_robot((8, 10), 1)

        actions = {
            (10, 10): ['move', (9, 10)],
            (11, 10): ['move', (10, 10)],
            (12, 10): ['move', (11, 10)],
            (8, 10): ['move', (9, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((10, 10)))
        self.assertEqual(state2.robots[10, 10].hp,
                         settings.robot_hp - settings.collision_damage*2)
        self.assertTrue(state2.is_robot((11, 10)))
        self.assertEqual(state2.robots[11, 10].hp,
                         settings.robot_hp - settings.collision_damage*2)
        self.assertTrue(state2.is_robot((12, 10)))
        self.assertEqual(state2.robots[12, 10].hp,
                         settings.robot_hp - settings.collision_damage)
        self.assertTrue(state2.is_robot((8, 10)))
        self.assertEqual(state2.robots[8, 10].hp,
                         settings.robot_hp - settings.collision_damage)

    def test_try_swap(self):
        state = GameState()
        state.add_robot((9, 9), 0)
        state.add_robot((8, 9), 1)

        actions = {
            (9, 9): ['move', (8, 9)],
            (8, 9): ['move', (9, 9)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 9)))
        self.assertEqual(state2.robots[9, 9].player_id, 0)
        self.assertEqual(state2.robots[9, 9].robot_id,
                         state.robots[9, 9].robot_id)
        self.assertEqual(state2.robots[9, 9].hp,
                         settings.robot_hp - settings.collision_damage)
        self.assertTrue(state2.is_robot((8, 9)))
        self.assertEqual(state2.robots[8, 9].player_id, 1)
        self.assertEqual(state2.robots[8, 9].robot_id,
                         state.robots[8, 9].robot_id)
        self.assertEqual(state2.robots[8, 9].hp,
                         settings.robot_hp - settings.collision_damage)

    def test_try_move_in_circle(self):
        state = GameState()
        state.add_robot((8, 8), 0)
        state.add_robot((9, 8), 1)
        state.add_robot((9, 9), 0)
        state.add_robot((8, 9), 1)

        actions = {
            (8, 8): ['move', (9, 8)],
            (9, 8): ['move', (9, 9)],
            (9, 9): ['move', (8, 9)],
            (8, 9): ['move', (8, 8)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 8)))
        self.assertEqual(state2.robots[9, 8].hp, settings.robot_hp)
        self.assertEqual(state2.robots[9, 8].player_id, 0)
        self.assertTrue(state2.is_robot((9, 9)))
        self.assertEqual(state2.robots[9, 9].hp, settings.robot_hp)
        self.assertEqual(state2.robots[9, 9].player_id, 1)
        self.assertTrue(state2.is_robot((8, 9)))
        self.assertEqual(state2.robots[8, 9].hp, settings.robot_hp)
        self.assertEqual(state2.robots[8, 9].player_id, 0)
        self.assertTrue(state2.is_robot((8, 8)))
        self.assertEqual(state2.robots[8, 8].hp, settings.robot_hp)
        self.assertEqual(state2.robots[8, 8].player_id, 1)

    def test_unobvious_collision(self):
        state = GameState()
        state.add_robot((9, 10), 0)
        state.add_robot((9, 12), 1)
        state.add_robot((9, 11), 0)
        state.add_robot((11, 11), 1)

        actions = {
            (9, 10): ['move', (9, 11)],
            (9, 12): ['move', (9, 11)],
            (9, 11): ['move', (10, 11)],
            (11, 11): ['move', (10, 11)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 10)))
        self.assertEqual(state2.robots[9, 10].hp, settings.robot_hp)
        self.assertTrue(state2.is_robot((9, 12)))
        self.assertEqual(state2.robots[9, 12].hp,
                         settings.robot_hp - settings.collision_damage)
        self.assertTrue(state2.is_robot((9, 11)))
        self.assertEqual(state2.robots[9, 11].hp,
                         settings.robot_hp - settings.collision_damage*2)
        self.assertTrue(state2.is_robot((11, 11)))
        self.assertEqual(state2.robots[11, 11].hp,
                         settings.robot_hp - settings.collision_damage)

    def test_double_collision(self):
        state = GameState()
        state.add_robot((9, 10), 0)
        state.add_robot((10, 11), 0)
        state.add_robot((11, 10), 1)

        actions = {
            (9, 10): ['move', (10, 10)],
            (10, 11): ['move', (10, 10)],
            (11, 10): ['move', (10, 10)]
        }

        state2 = state.apply_actions(actions, spawn=False)

        self.assertTrue(state2.is_robot((9, 10)))
        self.assertEqual(state2.robots[9, 10].hp,
                         settings.robot_hp - settings.collision_damage)
        self.assertTrue(state2.is_robot((10, 11)))
        self.assertEqual(state2.robots[10, 11].hp,
                         settings.robot_hp - settings.collision_damage)
        self.assertTrue(state2.is_robot((11, 10)))
        self.assertEqual(state2.robots[11, 10].hp,
                         settings.robot_hp - settings.collision_damage*2)
