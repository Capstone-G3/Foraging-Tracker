from django.db.models import Model, ForeignKey, DateField

from foraging_app.models import user, marker


class User_Marker(Model):
    user_id = ForeignKey(user.User)
    marker_id = ForeignKey(marker.Marker)
    saved_date = DateField(auto_now=True)


    def getMarkers(self, targetUser: user.User):
        target_id = targetUser.id
        marker_ids = User_Marker.objects.filter(user_id=target_id).values_list('marker_id', flat=True)
        markers = []
        for x in marker_ids:
            markers.append(marker.Marker.objects.get(id=x))
        return markers
