from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.db.models import (Model, AutoField, CharField, IntegerField, DateField, ImageField, BooleanField, ManyToManyField, EmailField)
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from foraging_app.models import group

'''I needed to use the base manager so that way i could override the default django user. This was the only way
to allow a user object to be created. We will have to do further modification to get the superuser working.
Since we have an update friday im going to leave this alone'''
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser):
    id = AutoField(primary_key=True)
    username = CharField(max_length=120, null=False, unique=True)
    '''I changed the email field to be apart of the user model. This makes it easier to implement default django functionality'''
    email = EmailField(max_length=254, default=None, null=False)
    password = CharField(max_length=64, null=False)
    rating = IntegerField(default=0)
    badge = [("Diamond", 100000), ("Platinum", 10000), ("Gold", 1000), ("Silver", 100), ("Bronze", 0)]
    profile_image = ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=False)
    created_since = DateField(auto_now=True, null=False)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_active = BooleanField(default=True) #we need to have this field as per django

    object = UserManager()
    USERNAME_FIELD = 'username'

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
        self.set_password(password) # this will use django to hash the password
        self.save()

    #returns None if valid, otherwise returns validation error
    def __validatePassword(self, password: str):
        return validate_password(password)

    def getGroups(self):
        from foraging_app.models.group import Group #doesn't cause circular import
        from foraging_app.models.user_group import User_Group
        targetID = self.id
        groupIDs = User_Group.objects.filter(user_id=targetID).values_list('group_id', flat=True)
        groups = []
        for x in groupIDs:
            groups.append(Group.objects.get(id=x))
        return groups

    def getName(self):
        return self.username