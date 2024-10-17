from folium import Popup
from bs4 import BeautifulSoup # Using DOM to detect HTML injection.
from html import escape # Prevent XSS forbidden characters.

class MarkerContent:
    """
        A Popup Wrapper for Marker on Map.
    """

    def __init__(self):
        self.raw_html="""
        <div class='image-container'>
            <img src='{image_url}',height=100, width=100>
        </div>
        <div class='title-container'>
            <h3>{species_name}</h3>
            <p >{species_full_name}</p>
        </div>
        <div class='information-container'>
            <span>
                <p>Location : {latitude} , {longitude}</p>
            </span>
            <p>Category : {category}</p>
            <p>Description : {description}</p>
        </div>
        <a href='{marker_ref}'>{marker_name}</a>
        """
        self.width = 200 # Predefined.
        self.height = 200 # Predefined.
        self.content = {}

    def getPopup(self,contents):
        """
            contents:
                image_url : Representation of Image Location
                species_name : The String of Species Name (in Short)
                species_full_name : The complete name of Species
                latitude : An integer represent the Latitude
                longitude : An integer represent the Longitude
                category : The String represent the category of Species
                description : The String description of marker.
                marker_ref : The URL refers to this marker
                marker_name : The title of the Marker.
            
            :return : The Popup Element from Folium to represent a Marker.
        """
        for key,value in contents.items():
            html_escaped = escape(value)
            if bool(BeautifulSoup(html_escaped, 'html.parser').find()):
                raise ValueError("Code detected in input Content.")
            else:
                self.content[key] = html_escaped
        parsed_html = self.raw_html.format(**self.content)
        return Popup(html=parsed_html, parse_html=False, lazy=True)
        