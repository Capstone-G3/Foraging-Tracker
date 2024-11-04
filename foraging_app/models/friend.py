from django.db.models import (Model, AutoField, CharField, IntegerField, DateField, ImageField, BooleanField,
                              ForeignKey, CASCADE, SET_NULL, DateTimeField, FloatField, TextField, Q)

from foraging_app.models.user import User


class Friend(Model):
    user_a = ForeignKey(User, on_delete=CASCADE, related_name='friend_a')
    user_b = ForeignKey(User, on_delete=CASCADE, related_name='friend_b')
    friend_since = DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_b.username

    def get_friends(self):
        return Friend.objects.filter(user_a=self).select_related('user_b')


class Friend_Request(Model):
    Status = (
        ("Accept", 0),
        ("Pending", 1),
        ("Reject", 2)
    )
    uid_sender = ForeignKey(User, on_delete=CASCADE, related_name='request_sender')
    uid_receiver = ForeignKey(User, on_delete=CASCADE, related_name='request_receiver')
    status = IntegerField(choices=Status, default=1)
    request_date = DateTimeField(auto_now=True)
