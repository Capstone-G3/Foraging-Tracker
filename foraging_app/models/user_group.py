from django.db.models import Model, ForeignKey

from foraging_app.models import user, group
from foraging_app.models.marker import Marker


class User_Group(Model):
    user_id = ForeignKey(user.User)
    group_id = ForeignKey(group.Group)


    def getGroupMembers(self, targetGroup: group.Group):
        target_id = targetGroup.id
        members_ids = User_Group.objects.filter(group_id=target_id).values_list('user_id', flat=True)
        members = []
        for x in members_ids:
            members.append(user.User.objects.get(id=x))
        return members

    def getGroupMarkers(self, targetGroup: group.Group):
        target_id = targetGroup.id
        member_ids = User_Group.objects.filter(group_id=target_id).values_list('user_id', flat=True)
        members = []
        for x in member_ids:
            members.append(user.User.objects.get(id=x))
        marker_owners = []
        markers = []
        for x in members:
            marker_owners = Marker.objects.filter(owner=x).values_list('id', flat=True)
            for y in marker_owners:
                markers.append(Marker.objects.get(id=y))
        return markers

    def existInGroup(self, member: user.User, targetGroup: group.Group)-> bool:
        return User_Group.objects.filter(group_id=targetGroup.id, user_id=member.id).exists()