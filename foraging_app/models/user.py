from django.db.models import (Model, AutoField, CharField, IntegerField, ForeignKey,
                              CASCADE, DateField, ImageField)

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


class UserProfile(Model):
    id = AutoField(primary_key=True)
    home_address = CharField(max_length=254, null=False)
    phone = CharField(max_length=15, default=None)
    gender = [("Male", 2), ("Female", 1), ("Other", 9)]
    user_id= ForeignKey(User, on_delete=CASCADE)