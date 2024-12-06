from django.forms import ModelForm, Select, CharField

from foraging_app.models import Species

CLASSIFICATION = [
    ('ANIMAL','Animal'),
    ('PLANT','Plant'),
    ('TREE','Tree'), 
    ('FRUIT','Fruit')]

class SpeciesCreateForm(ModelForm):
    breed = CharField(required=False)
    
    class Meta:
        model = Species
        fields = ['type_animal', 'category', 'breed']
        widgets = {
            'type_animal' : Select(choices=CLASSIFICATION),
            'category' : Select
        }
        
