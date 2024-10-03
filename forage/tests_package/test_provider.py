from unittest import TestCase
from forage.sitemap.providers import MapStyleProvider, providers_list
from xyzservices.lib import Bunch, TileProvider

class TestProvider(TestCase):
    
    def setUp(self):
        self.provider = MapStyleProvider()
        
    """ Test to ensure that all Providers remained Valid through life-cycle."""
    def test_style_map_valid_providers(self):
        """ For each of the provider in list, it is guaranteed to be either Bunch or TileProvider"""
        for provider in providers_list:
            self.assertIsNotNone(provider)
            self.assertTrue(isinstance(provider, Bunch) | isinstance(provider, TileProvider))
        
    def test_look_up_on_source(self):
        """
            This unit will test the a simple look up off the Available List.
        """
        tile_set = self.provider.source_lookup("OpenStreetMap")
        self.assertIsNotNone(tile_set)
        self.assertTrue(len(tile_set) != 0)

    def test_look_up_success_on_finding_correct_type(self):
        """
            This unit will test all retrieved element from a look up is Tile Provider for easy access.
        """
        all_tiles = self.provider.source_lookup("Stadia")
        self.assertIsNotNone(all_tiles)
        for tile in all_tiles:
            for name, prop in tile.items():
                self.assertTrue(isinstance(prop, TileProvider))

    def test_look_up_on_option_OpenStreetMap(self):
        """
            Test a search Map Option on OpenStreetMap Variation.
        """
        source = "OpenStreetMap"
        option_variation = "Mapnik"
        source_option = source + "." + option_variation
        look_up = self.provider.options_lookup(source, option_variation)[source_option]
        
        self.assertIsNotNone(look_up) # Look should be successful.
        self.assertTrue(isinstance(look_up, TileProvider)) # The type we look for is TileProvider for Map.
        self.assertEqual("https://tile.openstreetmap.org/{z}/{x}/{y}.png", look_up.url) # The correct link to host Tile.
        self.assertEqual(source_option, look_up.name) # The map should match, this is obvious from dictionary search.

    def test_look_up_on_option_fail(self):
        source = "OpenStreetMap"
        option_variation = "Mapniksssss"
        with self.assertRaises(KeyError, msg="Tile Option cannot be found.") as raiseException:
            look_up = self.provider.options_lookup(source, option_variation)
        self.assertEqual(str(raiseException.msg), "Tile Option cannot be found.")


    def test_look_up_on_option_source_fail(self):
        source = "OpenStreetMaps"
        with self.assertRaises(KeyError, msg="Invalid Tile Source") as raiseException:
            look_up = self.provider.source_lookup(source)
        self.assertEqual(raiseException.msg, "Invalid Tile Source")
