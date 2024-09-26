from folium import Icon, Marker, Map, Figure, CircleMarker, Popup, LayerControl
from folium.plugins import MiniMap, LocateControl, MarkerCluster, TagFilterButton

class BaseMap:
    map_source_tiles = "OpenStreetMap"
    center_zoom= 12
    # Longitude , Latitude max
    min_lon, max_lon = -180, 180
    min_lat, max_lat = -90, 90
    # Zoom Control
    zoom_control = True
    #Preserve Marker when Overscroll
    copy_on_jump = True
    #Max Bound Limit
    max_bounds = True

    def __init__(self):
        self.__figure__= Figure()
        self.__map__ = Map(
            zoom_start=self.center_zoom,
            world_copy_jump=self.copy_on_jump,
            max_bounds=self.max_bounds,
            min_lat= self.min_lat,
            max_lat=self.max_lat,
            min_lon=self.min_lon,
            max_lon=self.max_lon,
            zoom_control=self.zoom_control)
        locate_control = LocateControl(auto_start=True)
        self.__map__.add_child(locate_control)
        self.cluster = MarkerCluster()
        self.attr_layer = LayerControl(show=True)
        
    def add_marker(self,location:tuple, content:str):
        content_frame = Popup(content)
        element = Marker(location=location, popup=content_frame)
        self.cluster.add_child(element)
    
    def add_markers(self, locations:list, contents:list):
        for location in locations:
            self.add_marker(location)
    
    def add_zone_marker(self, location:tuple, radius:int):
        marker = CircleMarker(location=location, radius=radius)

    def render(self):
        self.__map__.add_child(self.cluster)
        self.__figure__.add_child(self.__map__)
        return self.__figure__.render()

# Desktop Map will contain Mini Map, allowed to be disabled. 
class DesktopMap(BaseMap):
    def __init__(self):
        super().__init__()
        self.mini = MiniMap()
        self.attr_layer.add_child(self.mini)

    #TODO
    def disable_mini(self):
        pass