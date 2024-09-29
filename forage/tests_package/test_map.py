from unittest import TestCase
from random import randint
from forage.sitemap.base import *

class TestSiteMap(TestCase):
    markers = []
    boilerplate = "<html> <p>{placeholder}</p> </html>"

    def setUp(self):
        # 10 Randomized Latitude and Longtitude
        for i in range(0,10):
            self.markers.append((randint(0,25), randint(0,50)))

    def test_base_map_do_not_contain_mini_map(self):
        """
            Based Map does not contain Mini Map
        """
        default_map = BaseMap()
        # A newly Map created shouldn't be None.
        self.assertIsNotNone(default_map)

        # Reflection to check for Mini-Map.
        map_dict = default_map.__dict__
        with self.assertRaises(KeyError):
            mini = map_dict["__mini__"] # KeyError because mini never exist
            self.assertIsNone(mini)

    def test_add_single_marker_successful_when_correct_location_and_content_parameter(self):
        """
            A unit test for adding a single marker to the BaseMap with additional customize contents.
            Base Map can add a single marker. 
        """
        default_map = BaseMap()
        # Replace Later for a Module represent Content of Marker.
        post_content = self.boilerplate.format(placeholder="Hello")

        default_map.add_marker(self.markers[0], post_content)
        self.assertEqual(len(default_map), 1)
        # Map only compiled when Figure do, therefore we need to check Cluster instead. (Cluster live inside the Map but it's a separate Component until Compile.)
        cluster_dict = default_map.__cluster__._children
        
        #First element second Field of Cluster children.
        added_marker = list(cluster_dict.items())[0][1]
        self.assertTrue(isinstance(added_marker, Marker))

        # There is only a single Marker, so a single element in the List, unpacking would be more efficient than a Loop.
        [(cluster_name, cluster_value)] = cluster_dict.items()
        # Cluster object holds all the information about Markers. 
        marker_dict = cluster_value._children.items()
        # The content we want to check is lay deep inside a Popup Object. (Popup lives inside Marker.)
        [(pop_key, pop_value)] = marker_dict
        # Pop_value represent the Popup object from Marker as the child.
        # Though it is not straight forward since Popup Object contain Wrapper for HTML element from Branca's Package.
        # To dig deeper, using reflection to find the item
        [(html_name, html_value)] = pop_value.html._children.items()
        # HTML_Value hold Branca HTML object which contain the Data we want to extract to see if it is the same as the User post earlier.
        self.assertEqual(html_value.data, post_content)
        
    
    def test_add_single_marker_fails_when_none_content(self):
        """
            When adding a marker to the map, content must specified before it must be add into the Map.
            In this case, marker can not be added because content is None.
        """
        default_map = BaseMap()
        # When creating a Marker without Content, it is necessary to stop operation.
        with self.assertRaises(ValueError, msg="Content is Empty"):
            # Adding Operation.
            default_map.add_marker(self.markers[0], content=None)
        # If operation is terminated, then adding never happen.
        self.assertEqual(len(default_map), 0)

    def test_add_single_marker_fails_when_content_empty(self):
        """
            Same as the above test, if content is not specified during Marker creation on the Map, it should fail.
            In this case, content is empty which an existing String.
        """
        default_map = BaseMap()
        # Adding marker with empty content with a valid location tuple.
        with self.assertRaises(ValueError, msg="Content is empty"):
            default_map.add_marker(location=self.markers[0], content='')
        # Operation is terminated.
        self.assertEqual(len(default_map), 0)

        #Through reflection to check BaseMap class (breaks encapsulation)
        cluster_children = list(default_map.__cluster__._children.items())
        self.assertEqual(len(cluster_children), 0)

    def test_add_single_marker_fails_when_location_empty(self):
        """
            When location is empty, there is no Marker being made.
        """
        default_map = BaseMap()
        with self.assertRaises(ValueError, msg="Illegal Location Format"):
            default_map.add_marker(location=(), content=self.boilerplate.format(placeholder="newly created"))
        self.assertEqual(len(default_map), 0)
    
    def test_add_single_marker_fails_when_location_incorrect_format(self):
        """
            Location must be in the correct format for parsing to happen for Marker Object.
        """
        default_map = BaseMap()
        with self.assertRaises(ValueError, msg="Illegal Location Format"):
            default_map.add_marker(location=(1, ), content=self.boilerplate.format(placeholder="newly created"))
        self.assertEqual(len(default_map), 0)

    def test_add_single_marker_fails_when_location_incorrect_type(self):
        """
            Same as above test, location must be in the correct format for parsing to happen for Marker Object.
        """
        default_map = BaseMap()
        # This one should be handled by Folium Marker itself.
        with self.assertRaises(ValueError):
            default_map.add_marker(location=("hello", "world"), content=self.boilerplate.format(placeholder="newly created"))
        self.assertEqual(len(default_map), 0)

    def test_add_multiple_marker_success_when_locations_and_contents_correct(self):
        """
            Adding multiple markers into the Map, using a list of dummy contents to put into the Marker.
            Both location and content array must be equals in size and must be in the correct format.
        """
        # Setup Contents for Multiple Markers
        default_map = BaseMap()
        list_contents = [
            "something",
            "more",
            "than",
            "just",
            "surprise",
            "it's amazing",
            "awesome",
            "working hard",
            "yeeeehawwww",
            "meowing?"
        ]
        marker_content = {}
        for marker, content in zip(self.markers, list_contents):
            marker_content[marker] = self.boilerplate.format(placeholder=content)
        self.assertEqual(len(marker_content), len(self.markers))

        # Making sure that Map contains the same N amount of marker_content have.
        default_map.add_markers(locations=list(marker_content.keys()), contents=list(marker_content.values()))
        self.assertEqual(len(default_map), len(marker_content))

        #Reflection to find Content element from Markers (Breaks Encapsulation)
        cluster_children = default_map.__cluster__._children.items()
        # Unpack each object value stored in Cluster.
        unpack_from_cluster = []
        for marker_name, marker_value in cluster_children:
            unpack_from_cluster.append(marker_value)
        # The amount of Children should be equivalent to markers added.
        self.assertEqual(len(unpack_from_cluster), len(marker_content))
        extract_data_from_marker = []
        for marker in unpack_from_cluster:
            marker_properties = list(marker._children.items())
            [(popup_name, popup_properties)] = marker_properties
            [(html_name, html_element)] = list(popup_properties.html._children.items())
            extract_data_from_marker.append(html_element.data)
        
        for data, original in zip(extract_data_from_marker, list_contents):
            self.assertEqual(data, self.boilerplate.format(placeholder=original))
    
    def test_add_multiple_marker_fails_when_none_content(self):
        """
          Base Map can add a list of Markers, this test does not add any custom contents to Marker.
          By adding no content to the Marker, it is not a valid Marker, so there must be Exception for handling.
        """
        default_map = BaseMap()
        with self.assertRaises(ValueError, msg="Illegal Content Format"):
            default_map.add_markers(self.markers, contents=None)
        self.assertEqual(len(default_map), 0)
    
    def test_add_multiple_marker_fails_when_empty_contents(self):
        """
            This unit will test setting contents to a list of empty String.
        """
        default_map = BaseMap()
        with self.assertRaises(ValueError, msg="Locations or Contents is empty."):
            default_map.add_markers(locations=self.markers, contents=['',''])
        self.assertEqual(len(default_map), 0)
    
    def test_add_multiple_marker_fails_when_locations_contents_different_length(self):
        """
            When Locations and Contents array size is different, some component will miss the other, therefore it
            can not be assumed to be correct. 
        """
        default_map = BaseMap()
        placeholders = [
            "Capstone",
            "Group",
            "3rd",
            "is the best"
        ]
        # Instead of looping, using high order function to do the job. Should remain O(n).
        f = lambda x : self.boilerplate.format(placeholder=x)
        list_contents = list(map(f,placeholders))
        # The two lists should have different length for this test.
        self.assertNotEqual(len(list_contents), len(self.markers))
        
        #The list of locations and contents do not have an even number of elements.
        # location.length -> 10
        # contents.length -> 4
        with self.assertRaises(ValueError, msg="Location and Content must contain even number of elements."):
            default_map.add_markers(locations=self.markers, contents=list_contents)
        # Operation terminated 
        self.assertEqual(len(default_map), 0)
            
    def test_add_multiple_marker_fails_when_locations_is_empty(self):
        """
            When a list of locations is empty, there is no Marker to be set on the Map.
        """
        default_map = BaseMap()
        # Valid Content
        post_content = [self.boilerplate.format(placeholder="Single Test")]
        with self.assertRaises(ValueError, msg="Locations or Contents is empty."):
            default_map.add_markers(locations=[], contents=post_content)
        self.assertEqual(len(default_map), 0)

    def test_desktop_map(self):
        """
            Desktop Map will contain a MiniMap
        """
        map_with_mini = DesktopMap()
        self.assertIsNotNone(map_with_mini)
        map_dict = map_with_mini.__dict__
        self.assertIsNotNone(map_dict["__mini__"])
        self.assertTrue(isinstance(map_dict["__mini__"], MiniMap))
    
    def test_desktop_map_contain_list_styles(self):
        # TODO : next Sprint plan.
        pass