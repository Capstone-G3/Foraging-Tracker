from folium import Marker, Map, Figure, LayerControl
from folium.plugins import MiniMap, LocateControl, MarkerCluster, TagFilterButton
from folium.raster_layers import TileLayer

from forage.sitemap.plugins import ToggleMarker, AutoMarker, UserLocate

from forage.sitemap.content import MarkerContent

GREEN_MARKER_SPEC = """new L.Icon({
                            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                            iconSize: [25, 41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowSize: [41, 41]
                        });
                    """

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
    center_zoom= 12
    zoom_control = False
    copy_on_jump = True
    max_bounds = True
    min_zoom = 3

    def __init__(self):
        self.__figure__= Figure()
        self.__map__ = Map(
            zoom_start=2.5,
            world_copy_jump=self.copy_on_jump,
            max_bounds=self.max_bounds,
            min_lon=self.MAX_BOUND['LONGITUDE'][0],
            max_lon=self.MAX_BOUND['LONGITUDE'][1],
            zoom_control=self.zoom_control,
            attributionControl=False,
            tiles=TileLayer(tiles="OpenStreetMap", show=True, name="Light Mode", min_zoom=self.min_zoom),
        )
        self.__locate_control__ = UserLocate(
            auto_start=True,
            locateOptions={"maxZoom":8},
            strings={
                "title" : "Retrieve current location.",
                "popup" : None,
            },
        ) #Getting position of user.
        self.__styles__ = []
        self.__cluster__ = MarkerCluster(control=False, overlay=False) # Grouping Markers as Cluster
        self.__attribute__ = LayerControl(position="bottomleft")
        self.__toggle_pin__ = ToggleMarker()
        self.__map_size__ = 0
        
        
    def add_marker(self,location, **contents):
        """
        Add a single Ping Marker in the Map, then update the size of the Object.
        
        Parameter
        ---
        :location: integer tuple
            An integer tuple represent a Marker, (latitude,longitude)
            *parameter is not optional.
        
        :**content: kwargs
            A dictionary defined with elements as,
                image_url : Representation of Image Location
                species_name : The String of Species Name (in Short)
                species_full_name : The complete name of Species
                category : The String represent the category of Species
                description : The String description of marker. 
        """
        if location is None:
            raise ValueError("Location is empty")
        if len(location) != 2:
            raise ValueError("Illegal Location Format")
        latitude, longitude = location
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Invalid Latitude or Longitude")
        if not contents:
            raise ValueError("Content is empty")
        
        element = Marker(location=location)
        content_frame = MarkerContent()

        element.add_child(content_frame.getPopup(contents['contents']))
        self.__cluster__.add_child(element)
        self.__map_size__ += 1
    
    def add_markers(self, locations, contents):
        """
        Add multiple Markers, utilized add_marker in iterations
        
        Parameter
        ---
        :locations: list of tuples
            The list of tuples as location (latitude,longitude)
        
        :contents: list of Dictionaries
            A list of dictionaries
        """
        if contents is None or len(contents) == 0:
            raise ValueError("Illegal Content Format")
        if len(locations) == 0:
            raise ValueError("Locations or Contents is empty.")
        if len(locations) != len(contents):
            raise ValueError("Location and Content must contain even number of elements.")
       

        for i in range(len(locations)):
            self.add_marker(location=locations[i], **contents[i])

    def set_map_error_message(self, error_message):
        self.__locate_control__.set_error_message(error_message)

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
        self.__map__.add_child(self.__attribute__)
        self.__map__.add_child(self.__locate_control__)
        self.__figure__.add_child(self.__map__)

        return self.__figure__
    
    def __len__(self):
        return self.__map_size__

class DesktopMap(BaseMap):
    """
    Desktop Map will contain Mini Map, allowed to be disabled through Layer Control.
    """ 
    _available = [
        TileLayer("CartoDB dark_matter", name="Dark Mode", show=False, min_zoom=BaseMap.min_zoom),
        TileLayer("Esri world_imagery", name="Satellite Mode", show=False, min_zoom=BaseMap.min_zoom),
    ] 

    def __init__(self):
        super().__init__()
        self.__mini__ = MiniMap().add_to(self.__map__)
        self.__styles__.extend(self._available)
        
    def compile_figure(self):
        return super().compile_figure() 

class PinMap(BaseMap):
    """
        Derived from Base Map, allow the User to select a point on the map and autofill Form for ease of finds.
    """
    def __init__(self):
        super().__init__()
        self.__pin__ = ToggleMarker()
        self.__auto_marker__ = AutoMarker()

    def compile_figure(self):
        self.__map__.add_child(self.__pin__)
        self.__map__.add_child(self.__auto_marker__)
        return super().compile_figure()  

class InformationMap:
    """
        A different type of Map for viewing a single
    """
    def __init__(self):
        self.__figure__ = Figure(width="300px", height="300px")
        self.__map__ = Map(
            dragging=False,
            min_zoom=3,
            max_zoom=8,
            zoom_control=True,
            scrollWheelZoom=False,
            doubleClickZoom=False,
            attributionControl=False
        )
        self.__cluster__ = MarkerCluster(control=False, overlay=False) # Grouping Markers as Cluster
        self.__map_size__ = 0

    def add_marker(self,location):
        self.__map__.add_child(Marker(location=location))
        self.__map__.location=location
    
    def compile_figure(self):
        self.__map__.add_child(self.__cluster__)
        self.__figure__.add_child(self.__map__)
        return self.__figure__
        

