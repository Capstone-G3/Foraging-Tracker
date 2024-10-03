from django.db.models import (Model, AutoField, CharField, IntegerField, DateField, ImageField, BooleanField,
                              ForeignKey, CASCADE, SET_NULL)

from foraging_app.models.user import User
from foraging_app.models.species import Species


class Marker(Model):
    id = AutoField(primary_key=True)
    title = CharField(max_length=120, null=False)
    latitude = IntegerField(null=False)
    longitude = IntegerField(null=False)
    is_private = BooleanField(default=False)
    owner = ForeignKey(User, on_delete=CASCADE, null=False)
    species = ForeignKey(Species, on_delete=SET_NULL)

    def save(self,**kwargs):
        super().save(**kwargs)

    def delete(self, **kwargs):
        super().delete(**kwargs)

    def getOwner(self):
        return User.objects.get(id=self.owner)

    def getSpecies(self):
        return Species.objects.get(id=self.species)

    def setPrivate(self, private: bool):
        self.is_private = private
        self.save()

    def __str__(self):
        return self.title