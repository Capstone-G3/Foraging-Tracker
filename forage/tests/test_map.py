from unittest import TestCase
from forage.sitemap import *

class TestSiteMap(TestCase):
    def setUp(self):
        self.map = BaseMap()

    # Based Map does not contain Mini Map
    def test_default_map(self):
        default_map = BaseMap()
        self.assertIsNotNone(default_map)
        map_dict = default_map.__dict__
        with self.assertRaises(KeyError):
            mini = map_dict["mini"] # KeyError because mini never exist
            self.assertIsNone(mini)
    
    # Desktop Map will contain a MiniMap
    def test_desktop_map(self):
        map_with_mini = DesktopMap()
        self.assertIsNotNone(map_with_mini)
        map_dict = map_with_mini.__dict__
        self.assertIsNotNone(map_dict["mini"])
        self.assertTrue(isinstance(map_dict["mini"], MiniMap))
        