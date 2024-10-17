from folium import Icon, Marker, Map, Figure, LayerControl, FeatureGroup
from folium.plugins import MiniMap, LocateControl, MarkerCluster, TagFilterButton
from folium.raster_layers import TileLayer
from typing import Union
from forage.sitemap.providers import MapStyleProvider

from foraging_app.forms.marker import MarkerCreateForm

from branca.element import MacroElement, Element, Html
from jinja2 import Template


from forage.sitemap.content import MarkerContent

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
        self.__map__.add_child(self.__toggle_pin__)
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



class ToggleMarker(MacroElement):
    """
        Toggle Marker Pin, once click a marker will appear, double click to disappear.
            Addition feature added : 
                Click on marker for Popup.
        
    """
    _template = Template(
        """
            {% macro script(this, kwargs) %}
                var currentMarker = null;  

                function toggleMarker(e) {
                    if (currentMarker) {
                        {{ this._parent.get_name() }}.removeLayer(currentMarker);
                        currentMarker = null;  
                    } else {
                        
                        var greenIcon = new L.Icon({
                            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                            iconSize: [25, 41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowSize: [41, 41]
                        });

                        currentMarker = L.marker(e.latlng, {icon : greenIcon}).addTo({{ this._parent.get_name() }});
                        var lat = e.latlng.lat;
                        var lng = e.latlng.lng;

                        currentMarker.dragging.enable();

                        currentMarker.on('click', function() {
                            currentMarker.bindPopup({{ this.popup }}).openPopup();
                        });

                        currentMarker.on('dblclick', function() {
                            {{ this._parent.get_name() }}.removeLayer(currentMarker);
                            currentMarker = null;
                        });
                    }
                };
                {{ this._parent.get_name() }}.on('click', toggleMarker);
            {% endmacro %}
        """
    ) 

    def __init__(self, popup: Union[Html, str, None] = None):
        super().__init__()
        self._name = "ToggleMarker"
        
        if isinstance(popup, Element):
            popup = popup.render()
        
        # TODO : Create marker right on marker
        self.popup = '"<strong>Latitude</strong> : " + lat + "<br> <strong>Longitude</strong>: " + lng'