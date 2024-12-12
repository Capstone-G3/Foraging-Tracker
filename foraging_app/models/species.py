from django.db.models import (Model, AutoField, CharField, ImageField)

class Species(Model):

    id = AutoField(primary_key=True)
    type_animal = CharField(max_length=120, unique=True, null=False, verbose_name="type")
    category = CharField(max_length=120, null=True)
    breed = CharField(max_length=120, null=True)
    # scope = CharField(max_length=120, null=False)
    # description = CharField(max_length=512)
    # image = ImageField(upload_to='species_images/', null=False)
    #image = ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=False)


    def save(self, **kwargs):
        super().save(**kwargs)

    def delete(self, **kwargs):
        super().delete(**kwargs)

    def __str__(self):
        return self

    def getMarkers(self):
        from foraging_app.models.marker import Marker
        
        targetID = self.id
        markerIDs = Marker.objects.filter(species=targetID).values_list('id', flat=True)
        markers = []
        for x in markerIDs:
            markers.append(Marker.objects.get(id=x))
        return markers
