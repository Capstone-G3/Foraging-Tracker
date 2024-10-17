from django.forms import ModelForm, ModelChoiceField, Select, Textarea, CharField
from foraging_app.models import Marker, Species

class MarkerCreateForm(ModelForm):
    species = ModelChoiceField(queryset=Species.objects.all(), widget=Select, required=False)
    class Meta:
        model = Marker
        fields = [
            'longitude',
            'latitude',
            'title',
            'is_private',
            'image',
            'description'
        ]
    
class MarkerEditForm(MarkerCreateForm):
    description = CharField(widget=Textarea())
    class Meta:
        model = Marker
        exclude = ['longitude','latitude','owner']