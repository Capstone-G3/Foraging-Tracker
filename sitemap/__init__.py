from folium import (Icon, Marker, Map, Figure)
from folium.plugins import MiniMap
from nicegui import ui

fig_attr = Figure()
map_attr = Map(
    location=(0,0),
    zoom_start = 3
)
map_attr.add_to(fig_attr)
miniMap = MiniMap()
map_attr.add_child(miniMap)

def getDefaultMap():
    return fig_attr.render()

def addMarkertoMap(location:tuple, map:Map):
    map.add_child(Marker(location=location))
    map.add_to(fig_attr)
    return fig_attr.render()