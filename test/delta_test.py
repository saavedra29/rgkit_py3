
import ast
import pkg_resources
import unittest

from rgkit.settings import settings
from rgkit.gamestate import GameState

map_data = ast.literal_eval(
    open(pkg_resources.resource_filename('rgkit', 'maps/default.py')).read())
settings.init_map(map_data)


def delta_for(deltas, loc):
    for d in deltas:
        if d.loc == loc:
            return d


class TestDelta(unittest.TestCase):
    def test_suicide(self):
        state = GameState()
        loc1 = (10, 11)
        dest1 = (10, 10)
        loc2 = (9, 10)

        state.add_robot(loc1, 0)
        state.add_robot(loc2, 1)

        actions = {
            loc1: ['move', dest1],
            loc2: ['suicide']
        }
        deltas = state.get_delta(actions)

        d_guard = delta_for(deltas, loc1)
        d_suicide = delta_for(deltas, loc2)

        self.assertEqual(d_guard.hp - d_guard.hp_end, d_suicide.damage_caused)

    def test_attack(self):
        state = GameState()
        loc1 = (10, 11)
        dest1 = (10, 10)
        loc2 = (9, 10)
        dest2 = dest1

        state.add_robot(loc1, 0)
        state.add_robot(loc2, 1)

        actions = {
            loc1: ['move', dest1],
            loc2: ['attack', dest2]
        }
        deltas = state.get_delta(actions)

        d_move = delta_for(deltas, loc1)
        d_attack = delta_for(deltas, loc2)

        self.assertEqual(d_move.hp - d_move.hp_end, d_attack.damage_caused)

    def test_simple_collision(self):
        state = GameState()
        loc1 = (10, 11)
        dest1 = (10, 10)
        loc2 = (9, 10)
        dest2 = dest1

        state.add_robot(loc1, 0)
        state.add_robot(loc2, 1)

        actions = {
            loc1: ['move', dest1],
            loc2: ['move', dest2]
        }

        deltas = state.get_delta(actions)

        d_move1 = delta_for(deltas, loc1)
        d_move2 = delta_for(deltas, loc2)

        self.assertEqual(d_move1.hp - d_move1.hp_end, d_move2.damage_caused)
        self.assertEqual(d_move2.hp - d_move2.hp_end, d_move1.damage_caused)

    def test_three_collision(self):
        state = GameState()
        loc1 = (10, 11)
        loc2 = (9, 10)
        loc3 = (11, 10)

        dest = (10, 10)

        state.add_robot(loc1, 0)
        state.add_robot(loc2, 1)
        state.add_robot(loc3, 1)

        actions = {
            loc1: ['move', dest],
            loc2: ['move', dest],
            loc3: ['move', dest]
        }

        deltas = state.get_delta(actions)

        d_player0 = delta_for(deltas, loc1)
        d_player1_1 = delta_for(deltas, loc2)
        d_player1_2 = delta_for(deltas, loc3)

        self.assertEqual(d_player0.hp - d_player0.hp_end,
                         d_player1_1.damage_caused + d_player1_2.damage_caused)

        player1_hp_lose = d_player1_1.hp - d_player1_1.hp_end + \
            d_player1_2.hp - d_player1_2.hp_end

        self.assertEqual(player1_hp_lose, d_player0.damage_caused)

    def test_collision_and_attack(self):
        state = GameState()
        loc1 = (10, 11)
        loc2 = (9, 10)
        loc3 = (11, 11)

        dest = (10, 10)
        attack_dest = loc1

        state.add_robot(loc1, 0)
        state.add_robot(loc2, 1)
        state.add_robot(loc3, 1)

        actions = {
            loc1: ['move', dest],
            loc2: ['move', dest],
            loc3: ['attack', attack_dest]
        }

        deltas = state.get_delta(actions)

        d_player0 = delta_for(deltas, loc1)
        d_player1_move = delta_for(deltas, loc2)
        d_player1_attack = delta_for(deltas, loc3)

        self.assertEqual(d_player1_move.damage_caused,
                         settings.collision_damage)

        self.assertTrue(settings.attack_range[0] <=
                        d_player1_attack.damage_caused <=
                        settings.attack_range[1])

        self.assertEqual(d_player0.hp - d_player0.hp_end,
                         d_player1_move.damage_caused +
                         d_player1_attack.damage_caused)

        player1_hp_lose = d_player1_move.hp - d_player1_move.hp_end + \
            d_player1_attack.hp - d_player1_attack.hp_end

        self.assertEqual(player1_hp_lose, d_player0.damage_caused)

    def test_spawn(self):
        state = GameState()
        deltas = state.get_delta(actions={}, spawn=True)
        for d in deltas:
            self.assertTrue(hasattr(d, 'damage_caused'))
