from django.db.models import (AutoField, IntegerField, DateField, CharField, ImageField, ForeignKey, Model, CASCADE)
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from foraging_app.settings import EMAIL_HOST_USER
import datetime

class User(AbstractUser):
    """
        Forage User Class with custom fields.
    """
    BADGE = (
        ("Diamond", 100000),
        ("Platinum", 10000),
        ("Gold", 1000),
        ("Silver", 100),
        ("Bronze", 10)
    )
    is_active=True

    id = AutoField(primary_key=True, editable=False)
    rating = IntegerField(default=0)
    profile_image = ImageField(upload_to='user_profile', null=False)
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
        if 'rating' in kwargs:
            self.rating = kwargs['rating']
        if 'profile_image' in kwargs:
            self.profile_image = kwargs['profile_image']
        self.save()

    def getName(self):
        return self.username

    def getGroups(self):
        from foraging_app.models.group import Group, User_Group # Possible change later for Refactor, bad design.
        targetID = self.id
        groupIDs = User_Group.objects.filter(user_id=targetID).values_list('group_id', flat=True)
        groups = []
        for x in groupIDs:
            groups.append(Group.objects.get(id=x))
        return groups


class User_Profile(Model):
    MALE=2
    FEMALE=1
    OTHER=9

    GENDER = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other")
    )
    
    id = AutoField(primary_key=True)
    home_address = CharField(max_length=254, null=False)
    phone = CharField(max_length=15, default=None)
    bio = CharField(max_length=500, blank=True)
    age = IntegerField(blank=True, null=True)
    birthday = DateField(auto_now=False, null=False, default=datetime.datetime(1000,1,1))
    gender= IntegerField(choices=GENDER,default=MALE)
    user_id= ForeignKey(User, on_delete=CASCADE)

    def get_home_address(self):
        return self.home_address
    
    def get_phone(self):
        return self.phone
    
    def get_gender(self):
        return self.gender