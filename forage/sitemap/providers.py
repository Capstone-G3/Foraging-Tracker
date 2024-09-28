# Reference : https://github.com/geopandas/xyzservices/blob/main/xyzservices/data/providers.json
import xyzservices.providers as providers
from folium.raster_layers import TileLayer

 # Dictionary Attribute Access Providers
providers_list = [
    providers.OpenStreetMap,
    providers.Stadia,
    providers.OpenSeaMap,
    providers.OPNVKarte,
    providers.OpenTopoMap,
    providers.OpenRailwayMap,
    providers.OpenFireMap,
    providers.SafeCast,
    providers.BaseMapDE,
    providers.CyclOSM,
    providers.Esri,
    providers.FreeMapSK,
    providers.MtbMap,
    providers.CartoDB,
    providers.HikeBike,
    providers.BasemapAT,
    providers.nlmaps,
    providers.NASAGIBS,
    providers.JusticeMap,
    providers.OneMapSG,
    providers.USGS,
    providers.WaymarkedTrails,
    providers.OpenAIP,
    providers.OpenSnowMap,
    providers.SwissFederalGeoportal,
    providers.TopPlusOpen,
    providers.Gaode,
    providers.Strava]

class MapStyleProvider:

    def __init__(self):
        self.__tile_sets__ = []
        for provider in providers_list:
            for source, value in provider.flatten().items():
             self.__tile_sets__.append({source : value})

    def source_lookup(self, source):
        result = []
        for tile_set in self.__tile_sets__:
            for name, value in tile_set.items():
                if source.lower() in name.lower():
                    result.append(tile_set)
        if len(result) == 0:
            raise KeyError("Invalid Tile Source")
        return result
            
    def options_lookup(self,tile_set, tile_option):
        options = self.source_lookup(tile_set)
        if len(options) == 0:
            raise ValueError("Invalid Tile Source Set.")
        
        for option in options:
            for component, value in option.items():
                if tile_option.lower() in component.lower():
                    return option
                
        raise KeyError("Tile Option cannot be found.")