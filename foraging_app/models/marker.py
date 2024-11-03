from django.db.models import (Model, AutoField, CharField, IntegerField, DateField, ImageField, BooleanField,
                              ForeignKey, CASCADE, SET_NULL, DateTimeField, FloatField)

from foraging_app.models.user import User

class Marker(Model):
    PRIVATE_CHOICE = {
        True : "Private",
        False : "Public"
    }

    id = AutoField(primary_key=True)
    title = CharField(null=False,max_length=120, verbose_name="name")
    latitude = FloatField(null=False,default=0)
    longitude = FloatField(null=False, default=0)
    is_private = BooleanField(default=False, choices=PRIVATE_CHOICE, verbose_name='mode')
    image = ImageField(upload_to='marker_images/', null=True)
    description = CharField(max_length=150, blank=True, default='')
    owner = ForeignKey(User, on_delete=CASCADE, null=False, blank=False)
    species = ForeignKey("foraging_app.Species", on_delete=SET_NULL, blank=True, null=True)
    created_date = DateTimeField(auto_now=True)

    def save(self,**kwargs):
        super().save(**kwargs)

    def delete(self, **kwargs):
        super().delete(**kwargs)

    def __str__(self):
        return self.title
    
class Like_Marker(Model):

    user_id = ForeignKey(User, on_delete=CASCADE)
    marker_id = ForeignKey(Marker, on_delete=CASCADE)
    saved_date = DateField(auto_now=True)

    # Move this to Views. (Complete)
    # def getLikes(self, targetMarker):
    #     target_id = targetMarker.id
    #     user_ids = Like_Marker.objects.filter(marker_id=target_id).values_list('user_id', flat=True)
    #     users = []
    #     for x in user_ids:
    #         users.append(User.objects.get(id=x))
    #     return users
    
class User_Marker(Model):

    user_id = ForeignKey(User, on_delete=CASCADE)
    marker_id = ForeignKey(Marker, on_delete=CASCADE)
    saved_date = DateField(auto_now=True)

    # Move this to Views.
    # def getMarkers(self, targetUser):
    #     target_id = targetUser.id
    #     marker_ids = User_Marker.objects.filter(user_id=target_id).values_list('marker_id', flat=True)
    #     markers = []
    #     for x in marker_ids:
    #         markers.append(Marker.objects.get(id=x))
    #     return markers