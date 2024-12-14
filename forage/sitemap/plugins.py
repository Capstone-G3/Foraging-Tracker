from branca.element import MacroElement, Element, Html
from jinja2 import Template
from folium import Marker

from folium.plugins import LocateControl

GREEN_MARKER_SPEC = """new L.Icon({
                            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                            iconSize: [25, 41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowSize: [41, 41]
                        });"""

class AutoMarker(MacroElement):
    _template= Template(
    """
        {% macro script(this,kwargs) %}
            var currentMarker = null;
            var latInput = document.getElementById('id_marker-latitude');
            var longInput = document.getElementById('id_marker-longitude');
            
            function updateMarker(){
                let lat = latInput.value;
                let lng = longInput.value;

                if(currentMarker){
                    {{this._parent.get_name()}}.removeLayer(currentMarker);
                    currentMarker = null;
                }

                var marker_icon = {{this._marker_spec}};
                let latlng = L.latLng(lat,lng);
                currentMarker = L.marker(latlng, {icon : marker_icon}).addTo({{ this._parent.get_name() }});
            }

            latInput.addEventListener('change', updateMarker);
            longInput.addEventListener('change', updateMarker);
        {% endmacro %}
    """
    )

    def __init__(self):
        super().__init__()
        self._name = "AutoMarker"
        self._marker_spec = GREEN_MARKER_SPEC

class ToggleMarker(MacroElement):
    """
        Toggle Marker Pin, once click a marker will appear, double click to disappear.
    """
    _template = Template(
        """
            {% macro script(this, kwargs) %}
                var currentMarker = null;  
                {{ this._parent.get_name() }}.on('click', toggleMarker);

                function toggleMarker(e) {
                
                    if (currentMarker) {
                        {{ this._parent.get_name() }}.removeLayer(currentMarker);
                        currentMarker = null;  
                    } else {
                        
                        var marker_icon = {{this._marker_spec}}

                        // Create a Marker
                        currentMarker = L.marker(e.latlng, {icon : marker_icon}).addTo({{ this._parent.get_name() }});

                        // Autofill into form by selecting DOM by ID
                        let latInput = document.getElementById('id_marker-latitude');
                        let longInput = document.getElementById('id_marker-longitude');

                        latInput.value = e.latlng.lat;
                        longInput.value = e.latlng.lng;

                        // Double click will remove the marker completely.
                        currentMarker.on('dblclick', function() {
                            {{ this._parent.get_name() }}.removeLayer(currentMarker);
                            currentMarker = null;
                        });
                    }
                };
            {% endmacro %}
        """
    ) 

    def __init__(self):
        super().__init__()
        self._name = "ToggleMarker"
        self._marker_spec = GREEN_MARKER_SPEC

class UserLocate(LocateControl):
    _template = Template("""
        {% macro script(this, kwargs) %}
                
            var {{this.get_name()}} = L.control.locate(
                {{this.options | tojson}} ,
            );

            {{this._parent.get_name()}}.off('locationerror');
            {{this._parent.get_name()}}._handleGeolocationError = function(err){
                message = err.code > 1 ? 'Timeout' : '{{this._error_message}}';
                this.fire('locationerror', {message: message});
            }
                         
            {{this.get_name()}}.addTo({{this._parent.get_name()}});
            {% if this.auto_start %}
                {{this.get_name()}}.start();

            {% endif %}

            
            // This only happens assumed that there is a form with the same ID.
            const lat_auto = document.getElementById('id_marker-latitude');
            const long_auto = document.getElementById('id_marker-longitude');
            {{this._parent.get_name()}}.on('locationfound', function(e){
                lat_auto.value = e.latitude;
                long_auto.value = e.longitude;
            });

        {% endmacro %}
        """)
    
    def __init__(self, error_message="Access Denied", auto_start=False, **kwargs):
        super().__init__(auto_start= auto_start, **kwargs)
        self._error_message = error_message
        self._name = "UserLocate"
    
    def set_error_message(self,message):
        self._error_message = message

class ClickMarker(Marker):
    _template = Template(
    """
        {% macro script(this,kwargs) %}
            var {{ this.get_name() }} = L.marker(
                {{ this.location|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
            {{ this.get_name() }}.on('click', centerView);

            function centerView(){
                {{ this._parent.get_name() }}.setView({{ this.location | tojson }});
            }
        {% endmacro %}
    """
    )
   
    pass
