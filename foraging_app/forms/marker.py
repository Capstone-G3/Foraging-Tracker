from django.forms import ModelForm, ModelChoiceField, Select, Textarea, CharField
from foraging_app.models import Marker, Species
from foraging_app.models.marker import Comment


class MarkerCreateForm(ModelForm):
    species = ModelChoiceField(queryset=Species.objects.all(), widget=Select, required=False, empty_label="New")
    class Meta:
        model = Marker
        fields = [
            'latitude',
            'longitude',
            'title',
            'is_private',
            'image',
            'description'
        ]
        widgets = {
            'description' : Textarea(attrs={'rows': 4, 'cols': 32}),
        }
    
class MarkerEditForm(MarkerCreateForm):
    description = CharField(widget=Textarea())
    class Meta:
        model = Marker
        exclude = ['longitude','latitude','owner']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']