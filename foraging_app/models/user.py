from django.db.models import (AutoField, IntegerField, CASCADE, DateField, ImageField)
from foraging_app.models import group
from foraging_app.models.user_group import User_Group

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail

from foraging_app.settings import EMAIL_HOST_USER

class User(AbstractUser):
    """
        Forage User Class with custom fields.
    """
    BADGE = [("Diamond", 100000), ("Platinum", 10000), ("Gold", 1000), ("Silver", 100), ("Bronze", 10)]

    id = AutoField(primary_key=True, editable=False)
    rating = IntegerField(default=0)
    profile_image = ImageField(upload_to='static/images', height_field=None, width_field=None, max_length=100, null=False)
    created_since = DateField(auto_now=True, null=False)

    def __str__(self):
        return self.username
    
    def email_user(self, subject, message, **extra):
        """
            Send Email from the application to the User's given email.
        """
        send_mail(subject,message,EMAIL_HOST_USER,[self.email], **extra)

    def save(self, **kwargs):
        super().save(**kwargs)

    def delete(self, **kwargs):
        super().delete(**kwargs)

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

    def getGroups(self):
        targetID = self.id
        groupIDs = User_Group.objects.filter(user_id=targetID).values_list('group_id', flat=True)
        groups = []
        for x in groupIDs:
            groups.append(group.Group.objects.get(id=x))
        return groups

    def getName(self):
        return self.username
