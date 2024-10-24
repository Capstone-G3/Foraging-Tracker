from django.db.models import Model, AutoField, CharField, ForeignKey, CASCADE, SET_NULL, BooleanField

from foraging_app.models.user import User
from foraging_app.models.marker import Marker

class Group(Model):
    PRIVATE_CHOICE = {
        True: "Private",
        False: "Public"
    }

    id = AutoField(primary_key=True)
    name = CharField(max_length=120, unique=True, null=False)
    # category = CharField(max_length=120, null=False)
    isPrivate = BooleanField(default=False, choices=PRIVATE_CHOICE, null=False)
    description = CharField(max_length=512)
    user_admin = ForeignKey(User, on_delete=CASCADE, null=False)


    def save(self, **kwargs):
        super().save(**kwargs)

    def delete(self, **kwargs):
        super().delete(**kwargs)

    def __str__(self):
        return self.name

    def getAdmin(self):
        return self.user_admin
    

class User_Group(Model):

    user_id = ForeignKey(User, on_delete=SET_NULL, null=True)
    group_id = ForeignKey(Group, on_delete=CASCADE)

    def getGroupMembers(self, targetGroup):
        target_id = targetGroup.id
        members_ids = User_Group.objects.filter(group_id=target_id).values_list('user_id', flat=True)
        members = []
        for x in members_ids:
            members.append(User.objects.get(id=x))
        return members

    def getGroupMarkers(self, targetGroup):
        target_id = targetGroup.id
        member_ids = User_Group.objects.filter(group_id=target_id).values_list('user_id', flat=True)
        members = []
        for x in member_ids:
            members.append(User.objects.get(id=x))
        marker_owners = []
        markers = []
        for x in members:
            marker_owners = Marker.objects.filter(owner=x).values_list('id', flat=True)
            for y in marker_owners:
                markers.append(Marker.objects.get(id=y))
        return markers

    def existInGroup(self, member, targetGroup):
        return User_Group.objects.filter(group_id=targetGroup.id, user_id=member.id).exists()
