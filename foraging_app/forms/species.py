from django.forms import ModelForm, Select, CharField, TextInput


from foraging_app.models import Species

CLASSIFICATION = [
    ('ANIMAL','Animal'),
    ('PLANT','Plant'),
    ('TREE','Tree'), 
    ('FRUIT','Fruit'),
    # ("FUNGI", 'Fungi')
    ]

class SpeciesCreateForm(ModelForm):
    breed = CharField(required=False, widget=TextInput(attrs={'list' : 'breed_list'}))
    category = CharField(required=False, widget=TextInput(attrs={'list' : 'category_list'}))
    
    class Meta:
        model = Species
        fields = ['type_animal', 'category', 'breed']
        widgets = {
            'type_animal' : Select(choices=CLASSIFICATION),
        }
        
