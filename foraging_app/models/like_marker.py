from django.db.models import Model, ForeignKey, DateField

from foraging_app.models import user, marker


class Like_Marker(Model):
    user_id = ForeignKey(user.User)
    marker_id = ForeignKey(marker.Marker)
    saved_date = DateField(auto_now=True)

    def getLikes(self, targetMarker: marker.Marker):
        target_id = targetMarker.id
        user_ids = Like_Marker.objects.filter(marker_id=target_id).values_list('user_id', flat=True)
        users = []
        for x in user_ids:
            users.append(user.User.objects.get(id=x))
        return users
