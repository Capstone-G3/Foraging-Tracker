from django.db.models import Model, ForeignKey, DateField, CASCADE

from foraging_app.models import user, marker


class User_Marker(Model):
    user_id = ForeignKey('foraging_app.User', on_delete=CASCADE)#user.User)
    marker_id = ForeignKey('foraging_app.Marker', on_delete=CASCADE) #marker.Marker)
    saved_date = DateField(auto_now=True)


    def getMarkers(self, targetUser):# user.User):
        from foraging_app.models.marker import Marker
        target_id = targetUser.id
        marker_ids = User_Marker.objects.filter(user_id=target_id).values_list('marker_id', flat=True)
        markers = []
        for x in marker_ids:
            markers.append(Marker.objects.get(id=x))
        return markers
