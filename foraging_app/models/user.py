from django.contrib.auth.password_validation import validate_password
from django.db.models import (Model, AutoField, CharField, IntegerField, DateField, ImageField)

from foraging_app.models import group
from foraging_app.models.user_group import User_Group


class User(Model):
    id = AutoField(primary_key=True)
    username = CharField(max_length=120, null=False, unique=True)
    password = CharField(max_length=64, null=False)
    rating = IntegerField(default=0)
    badge = [("Diamond", 100000), ("Platinum", 10000), ("Gold", 1000), ("Silver", 100), ("Bronze", 0)]
    profile_image = ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=False)
    created_since = DateField(auto_now=True, null=False)

    def save(self, **kwargs):
        super().save(**kwargs)

    def delete(self, **kwargs):
        super().delete(**kwargs)

    def __str__(self) -> str:
        return self.username


    def setProfileByField(self, **kwargs):
        if 'username' in kwargs:
            self.username = kwargs['name']
        if 'password' in kwargs:
            self.password = kwargs['password']
        if 'rating' in kwargs:
            self.rating = kwargs['rating']
        if 'profile_image' in kwargs:
            self.profile_image = kwargs['profile_image']
        self.save()

    def setPassword(self, password: str):
        self.password = password
        self.save()

    #returns None if valid, otherwise returns validation error
    def __validatePassword(self, password: str):
        return validate_password(password)

    def getGroups(self):
        targetID = self.id
        groupIDs = User_Group.objects.filter(user_id=targetID).values_list('group_id', flat=True)
        groups = []
        for x in groupIDs:
            groups.append(group.Group.objects.get(id=x))
        return groups

    def getName(self):
        return self.username