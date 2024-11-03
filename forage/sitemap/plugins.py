from branca.element import MacroElement, Element, Html
from jinja2 import Template

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

