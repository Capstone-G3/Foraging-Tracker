from django.db.models import (Model, AutoField, CharField, IntegerField, ForeignKey,
                              CASCADE, DateField, EmailField, ImageField)

from django.contrib.auth.models import AbstractUser

# class MyUserManager(BaseUserManager):
#     def create_user(self, username, password, rating, badge, profile_image, created_since):
#         if not username:
#             raise ValueError('Users must have username')
#         user = self.model(
#             username=username,
#             rating=rating,
#             badge=badge,
#             profile_image=profile_image,
#             created_since=created_since,
#         )
#         user.set_password(password)
#         user.save()
#         return user
    #def superuser?

class User(AbstractUser):
    BADGE = [("Diamond", 100000), ("Platinum", 10000), ("Gold", 1000), ("Silver", 100), ("Bronze", 10)]
    USERNAME_FIELD = 'username'

    id = AutoField(primary_key=True)
    username = CharField(max_length=120, null=False, unique=True)
    password = CharField(max_length=64, null=False)
    rating = IntegerField(default=0)
    profile_image = ImageField(upload_to='static/images', height_field=None, width_field=None, max_length=100, null=False)
    created_since = DateField(auto_now=True, null=False)

    def __str__(self):
        return self.username


class User_Profile(Model):
    id = AutoField(primary_key=True)
    first_name = CharField(max_length=120, null=False)
    last_name = CharField(max_length=120, null=False)
    email = EmailField(max_length=254, null=False)
    home_address = CharField(max_length=254, null=False)
    phone = CharField(max_length=15, default=None)
    gender = [("Male", 2), ("Female", 1), ("Other", 9)]
    user_id= ForeignKey(User, on_delete=CASCADE)