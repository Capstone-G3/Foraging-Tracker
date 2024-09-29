from folium import Icon, Marker, Map, Figure, CircleMarker, Popup, LayerControl, FeatureGroup
from folium.plugins import MiniMap, LocateControl, MarkerCluster, TagFilterButton
from folium.raster_layers import TileLayer
from forage.sitemap.providers import MapStyleProvider

#TODO : Secure class to represent the Content for Markers.
class BaseMap:
    """
    Create a Default Map Object, an Interface Map for other various type of Maps.

    Parameter
    ---
    :map_source_tiles: str
        The Tile Set name for rendering the Map.
        default: 'OpenStreetMap'

    :center_zoom: integer
        The zoom level when Map is render.
        default: 12

    :zoom_control: bool
        The Button for Zooming In and Out
        default: True

    :copy_on_jump: bool
        Preserve the markers if the Map happened to Overscroll.
        default : True

    :max_bounds: bool
        Allow user to scroll out of bounds as repetition.
        default : True

    Field
    ---
    :figure: Figure
        Figure Object to render all Components.

    :map : Map
        Parent to all Maps' Components

    :locate_control: LocateControl
        Locating the user's location through GPS or allowed shared Location.
        All map must contain locate_control as default.
    
    :cluster: MarkerCluster
        The ability to group Markers at certain Zoom Level.
        All map must have cluster controls.

    :map_size: integer
        Indication of the number of Markers placed inside the Map.    
    
    Constant
    ---
    Prevent user to drag of the Minimum and Maximum Zone both Longitude & Latitude.

    :MIN_LONGITUDE: integer
        The Minimum Longitude of the Map
    
    :MAX_LONGITUDE: integer
        The Maximum Longitude of the Map
    
    :MIN_LATITUDE: integer
        The Minimum Latitude of the Map
    
    :MAX_LATITUDE: integer
        The Maximum Latitude of the Map
    """

    # Constant
    MAX_BOUND = {'LONGITUDE' : (-180,180), 'LATITUDE' : (-90,90)}

    map_source_tiles = "OpenStreetMap"
    center_zoom= 12
    zoom_control = False
    copy_on_jump = True
    max_bounds = True
    min_zoom = 2.5

    def __init__(self, tile_source=map_source_tiles):
        self.__figure__= Figure()
        self.__map__ = Map(
            zoom_start=self.center_zoom,
            world_copy_jump=self.copy_on_jump,
            max_bounds=self.max_bounds,
            min_lon=self.MAX_BOUND['LONGITUDE'][0],
            max_lon=self.MAX_BOUND['LONGITUDE'][1],
            zoom_control=self.zoom_control,
            tiles=None
            )
        locate_control = LocateControl(auto_start=True, strings={"title" : "Failed to get location."}) #Getting position of user.
        self.__map__.add_child(locate_control)
        self.__styles__ = [TileLayer(tiles=tile_source)]
        self.__cluster__ = MarkerCluster() # Grouping Markers as Cluster
        self.__attribute__ = LayerControl(position="bottomleft")
        self.__map_size__ = 0

        
    def add_marker(self,location,content):
        """
        Add a single Ping Marker in the Map, then update the size of the Object.
        
        Parameter
        ---
        :location: integer tuple
            An integer tuple represent a Marker, (latitude,longitude)
            *parameter is not optional.
        
        :content: str
            The Pseudo Content represent by String to be embedded inside Marker.
            *parameter  is not optional.
        
        """
        if location is None:
            raise ValueError("Location is empty")
        if len(location) > 2 or len(location) < 2:
            raise ValueError("Illegal Location Format")
        if content is None or content == '':
            raise ValueError("Content is empty")
        
        element = Marker(location=location)
        content_frame = Popup(content, lazy=True)
        element.add_child(content_frame)
        self.__cluster__.add_child(element)
        self.__map_size__ += 1
    
    def add_markers(self, locations, contents):
        """
        Add multiple Markers, utilized add_marker in iterations
        
        Parameter
        ---
        :locations: list of tuples
            The list of tuples as location (latitude,longitude)
        
        :contents: list of String
            The list of Strings to add contents to each marker
            A Pseudo Map :
                locations[0] -> contents[0]
        """
        if contents is None:
            raise ValueError("Illegal Content Format")
        if len(locations) == 0 or len(contents) == 0:
            raise ValueError("Locations or Contents is empty.")
        if len(locations) != len(contents):
            raise ValueError("Location and Content must contain even number of elements.")
       

        for i in range(len(locations)):
            self.add_marker(location=locations[i], content=contents[i])
            

    def compile_figure(self):
        """
        Figure will be returned for rendering Map in HTML.

        Note
        ---
        Please note that render must be the last call, please set up Map first.
        Returned Figure.render() can be use to display HTML
        
        :return: Figure Class.
        """ 
        for style in self.__styles__:
            self.__map__.add_child(style)
        self.__map__.add_child(self.__cluster__)
        self.__figure__.add_child(self.__map__)
        self.__map__.add_child(self.__attribute__)
        return self.__figure__
    
    def __len__(self):
        return self.__map_size__

class DesktopMap(BaseMap):
    """
    Desktop Map will contain Mini Map, allowed to be disabled through Layer Control.
    TODO : Additional Requirement is needed for Desktop Map.
    TODO : Mini Map styling
    
    
    """ 
    _available = [TileLayer("CartoDB dark_matter")] # TODO, add more styles to Layer Control.

    def __init__(self):
        super().__init__()
        self.__mini__ = MiniMap().add_to(self.__map__)
        self.__styles__.extend(self._available)
        
    def compile_figure(self):
        return super().compile_figure() 
