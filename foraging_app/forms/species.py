from django.forms import ModelForm, Textarea

from foraging_app.models import Species

class SpeciesCreateForm(ModelForm):
    class Meta:
        model = Species
        fields = ['name', 'category', 'scope','description']
        exclude = ['image']
        widgets= [
            {'description' : Textarea()}
        ]