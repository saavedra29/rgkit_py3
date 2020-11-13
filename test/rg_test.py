import ast
import pkg_resources
import unittest

from rgkit.settings import settings
from rgkit import rg

map_data = ast.literal_eval(
    open(pkg_resources.resource_filename('rgkit', 'maps/default.py')).read())
settings.init_map(map_data)


class TestRG(unittest.TestCase):
    def test_center(self):
        self.assertEqual(rg.CENTER_POINT, (9, 9))

    def test_types_invalid(self):
        self.assertEqual(rg.loc_types((-1, 9)), set(['invalid']))

    def test_types_spawn(self):
        self.assertEqual(rg.loc_types((3, 4)), set(['normal', 'spawn']))

    def test_types_obstacle(self):
        self.assertEqual(rg.loc_types((16, 4)), set(['normal', 'obstacle']))

    def test_types_normal(self):
        self.assertEqual(rg.loc_types((7, 2)), set(['normal']))

    def test_around(self):
        filtered = set(rg.locs_around((3, 3)))
        self.assertEqual(filtered, set([(3, 2), (4, 3), (3, 4), (2, 3)]))

    def test_around_filter(self):
        filtered = set(rg.locs_around((3, 3), filter_out=['obstacle']))
        self.assertEqual(filtered, set([(4, 3), (3, 4)]))

    def test_toward(self):
        self.assertTrue(rg.toward((5, 13), (8, 3)) in [(5, 12), (6, 13)])

    def test_toward_obstacle(self):
        self.assertEqual(rg.toward((5, 2), (4, 3)), (5, 3))
