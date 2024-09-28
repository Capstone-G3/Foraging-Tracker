from unittest import TestCase
from random import randint
from forage.sitemap.base import *

class TestSiteMap(TestCase):
    markers = []
    # 10 Randomized Latitude and Longtitude
    def setUp(self):
        for i in range(0,10):
            self.markers.append([randint(0,25), randint(0,50)])

    # Based Map does not contain Mini Map
    def test_default_map(self):
        default_map = BaseMap()
        # A newly Map created shouldn't be None.
        self.assertIsNotNone(default_map)

        # Reflection to check for Mini-Map.
        map_dict = default_map.__dict__
        with self.assertRaises(KeyError):
            mini = map_dict["mini"] # KeyError because mini never exist
            self.assertIsNone(mini)
    
    # Base Map can add a single marker, 
    # it can be proven by checking built in accessor size or Reflection on Cluster.
    # -> User can add a single Marker to the Map.
    def test_default_can_add_marker_no_content(self):
        default_map = BaseMap()
        default_map.add_marker(self.markers[0])
        self.assertEqual(len(default_map), 1) 

        # Double Check through Reflection
        cluster = default_map.__dict__['__cluster__']
        cluster_dict = list(cluster._children.items())
        # There is only a single marker
        self.assertEqual(len(cluster_dict),1)
        # Is it truly a Marker? OrderedDict{'marker' : Marker<Object>}
        self.assertTrue(isinstance(cluster_dict[0][1], Marker))

    # Base Map can add a list of Markers
    def test_default_can_add_multiple_marker_no_content(self):
        default_map = BaseMap()
        default_map.add_markers(self.markers)
        self.assertEqual(len(default_map), len(self.markers))

        # Through Reflection 
        cluster = default_map.__dict__['__cluster__']
        cluster_dict = list(cluster._children.items())
        # Cluster Dict shouldn't be None because it contains N of markers.
        self.assertIsNotNone(cluster_dict)
        # Two Dictionaries must be the same length.
        self.assertEqual(len(cluster_dict), len(self.markers))
        # Each Marker in Dict is an Instance of Folium Marker.
        for key,marker in cluster_dict:
            self.assertTrue(isinstance(marker, Marker))

    def test_default_fail_add_marker_no_content(self):
        pass

    def test_default_fail_add_multi_marker_no_content(self):
        pass

    def test_default_can_add_single_marker_with_content(self):
        pass

    def test_default_can_add_multiple_markers_with_content(self):
        pass

    def test_default_fail_add_single_marker_with_content(self):
        pass

    def test_default_fail_add_multiple_marker_with_content(self):
        pass

    def test_desktop_map(self):
        """Desktop Map will contain a MiniMap"""
        map_with_mini = DesktopMap()
        self.assertIsNotNone(map_with_mini)
        map_dict = map_with_mini.__dict__
        self.assertIsNotNone(map_dict["__mini__"])
        self.assertTrue(isinstance(map_dict["__mini__"], MiniMap))

    """ Test if new Map created contain Style Components"""
    def test_style_map(self):
        style_map = StyleMap()

    """ Test if Style Map able to change components"""
    def test_style_map_components(self):
        pass
