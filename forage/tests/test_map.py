from unittest import TestCase
from forage.sitemap import *

class TestSiteMap(TestCase):
    def setUp(self):
        self.map = BaseMap()

    def test_default_map(self):
        default_map = BaseMap()
        self.assertIsNotNone(default_map)
    
    # Desktop map should not have any Mini Map
    def test_desktop_map(self):
        map_with_mini = DesktopMap()
        self.assertIsNotNone(map_with_mini)
        
        