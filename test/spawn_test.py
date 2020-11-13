import ast
import pkg_resources
import unittest

from rgkit.settings import settings
from rgkit.gamestate import GameState

map_data = ast.literal_eval(
    open(pkg_resources.resource_filename('rgkit', 'maps/default.py')).read())
settings.init_map(map_data)


class TestSpawn(unittest.TestCase):
    def test_first_turn_spawning(self):
        state = GameState()

        actions = {}

        state2 = state.apply_actions(actions)

        self.assertEqual(state2.get_scores(),
                         [settings.spawn_per_player,
                          settings.spawn_per_player])

    def test_spawn_kills(self):
        state = GameState()

        state.add_robot((4, 3), 0)

        actions = {
            (4, 3): ['guard']
        }

        state2 = state.apply_actions(actions)

        self.assertTrue(not state2.is_robot((4, 3)) or
                        state2.robots[(4, 3)].robot_id !=
                        state.robots[4, 3].robot_id)

    def test_spawn_dodge(self):
        state = GameState()

        state.add_robot((4, 3), 0)

        actions = {
            (4, 3): ['move', (4, 4)]
        }

        state2 = state.apply_actions(actions)

        self.assertTrue(state2.is_robot((4, 4)))

    def test_spawn_dodge_overwrite(self):
        state = GameState()

        state.add_robot((4, 3), 0)

        actions = {
            (4, 3): ['move', (4, 4)]
        }

        # ensure that a robot will get spawned at (4, 3)
        state._get_spawn_locations = lambda: [(i, 3) for i in range(10)]

        state2 = state.apply_actions(actions)

        self.assertTrue(state2.is_robot((4, 4)))
        self.assertTrue(state2.is_robot((4, 3)))

    def test_spawn_hop_in(self):
        state = GameState()

        state.add_robot((4, 4), 0)

        actions = {
            (4, 4): ['move', (4, 3)]
        }

        state2 = state.apply_actions(actions)

        self.assertTrue(not state2.is_robot((4, 3)) or
                        state2.robots[(4, 3)].robot_id !=
                        state.robots[4, 4].robot_id)
