from folium import Popup
from bs4 import BeautifulSoup # Using DOM to detect HTML injection.
from html import escape # Prevent XSS forbidden characters.
from django.template import Template, Context

class MarkerContent:
    """
        A Popup Wrapper for Marker on Map.
    """

    def __init__(self):
        self.raw_html="""
        <div class='image-container'>
            <img src='{{marker.image.url}}'>
        </div>
        <div class='information-container'>
            <div>
                <strong>{{marker.title}}</strong> 
                {%if request.user.is_authenticated and request.user.id == owner.id%}
          
                <a href="{% url 'edit_marker' marker_id=marker.id%}">
                    {%load static%}
                    <img src="{% static 'img/edit-marker.svg' %}" alt="{{marker.title}}" width="20">
                </a>
                {%endif%}
            </div>
            <div>Owner : <a href="{% url 'user' userId=owner.id%}">@{{owner.username}}</a></div>
            <div>Location: {{marker.latitude}},{{marker.longitude}}</div>
            {%if marker.species.category%}
            <div>Category : {{marker.species.category}}</div>
            {%endif%}
            <div>Description : {{marker.description}}</div>
            <div><a href="{%url 'info_marker' marker_id=marker.id%}"> View More...</a></div>
        </div>

        """

    def getPopup(self,contents):
        """
            Using Django Template to render inside popup.
        """
        template = Template(self.raw_html)
        context = Context({**contents})
        parsed_html = template.render(context)
        return Popup(html=parsed_html, parse_html=False, lazy=True, offset=(-170,125))
        