import json
import random
import unittest

from rgkit.gamestate import GameState
from rgkit.settings import settings


class TestJson(unittest.TestCase):
    game1 = {
        'seed': '0',
        'turn': '12',
        'robots': [
            {
                'location': ['10', '12'],
                'hp': '50',
                'player_id': '0',
                'robot_id': '5',
            },
            {
                'location': ['10', '10'],
                'hp': '50',
                'player_id': '1',
                'robot_id': '6',
            }
        ],
    }

    actions1 = [
        {
            'location': ['10', '12'],
            'action': ['move', ['10', '11']],
        },
        {
            'location': ['10', '10'],
            'action': ['attack', ['10', '11']],
        }
    ]

    result1 = {
        'seed': '----',  # Randomized.
        'turn': '13',
        'robots': [
            {
                'location': ['10', '11'],
                'hp': '----',  # Randomized.
                'player_id': '0',
                'robot_id': '5',
            },
            {
                'location': ['10', '10'],
                'hp': '50',
                'player_id': '1',
                'robot_id': '6',
            }
        ],
    }

    def sprint(self, val):
        # Oh man why, oh why.
        def to_str(data):
            if isinstance(data, dict):
                for k, v in list(data.items()):
                    data[k] = to_str(v)
            elif isinstance(data, list) or isinstance(data, tuple):
                new_data = []
                for v in data:
                    new_data.append(to_str(v))
                data = new_data
            else:
                data = str(data)
            return data
        return json.dumps(to_str(val), sort_keys=True)

    def test_load_json_game_state(self):
        # Dump and load to validate
        data = json.loads(json.dumps(self.game1))
        state = GameState.create_from_json(data)
        info = state.get_game_info(json=True, seed=True)

        self.assertEqual(self.sprint(self.game1), self.sprint(info))

    def test_load_json_actions(self):
        data = json.loads(json.dumps(self.actions1))
        moves = GameState.create_actions_from_json(data)

        self.assertTrue((10, 12) in moves)
        self.assertEqual(json.dumps(moves[(10, 12)]),
                         json.dumps(['move', [10, 11]]))

    def test_apply_actions(self):
        state = GameState.create_from_json(self.game1)
        moves = GameState.create_actions_from_json(self.actions1)
        new_state = state.apply_actions(moves)
        info = new_state.get_game_info(json=True, seed=True)

        # TODO: Less mysterious randomization please -_-.
        r1 = random.Random('0' + 's')
        self.result1['seed'] = str(r1.randint(0, settings.max_seed))
        r2 = random.Random('0' + 'a')
        hp_left = 50 - r2.randint(*settings.attack_range)
        self.result1['robots'][0]['hp'] = hp_left

        self.assertEqual(self.sprint(self.result1), self.sprint(info))
