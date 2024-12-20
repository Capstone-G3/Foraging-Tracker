from django.db.models import (Model, IntegerField,
                              ForeignKey, CASCADE, DateTimeField, OneToOneField,
                              ManyToManyField)

from foraging_app.models.user import User
from foraging_app.models.marker import Marker


class Friend(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='user')
    friends = ManyToManyField(User, blank=True, related_name='friends')
    friend_since = DateTimeField(auto_now=True)
    shared_markers = ManyToManyField(Marker, blank=True, related_name='shared_markers')

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Adds a friend, if relationship doesn't exist yet // core functionality
        """
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        """
        Removes a friend, if relationship exists // core functionality
        """
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self, account):
        """
        Initiate the action of unfriending users // logic check.
        Delete Friend Request object from terminated friend relationship
        """

        user_friends_list = self
        user_friends_list.remove_friend(account)

        friend_list = Friend.objects.get(user=account)
        friend_list.remove_friend(self.user)

    def is_friend(self, account):
        """
        Checks if a friend is friend
        """
        # if account in self.friends.all():  # check account (user 2) is friends with user 1 return true is so
        #     return True
        user_friend_list = Friend.objects.get(user=self)
        friends = user_friend_list.friends.all()
        for friend in friends:
            if friend == account:
                return True


class Friend_Request(Model):
    Status = (
        ("Accept", 0),
        ("Pending", 1),
        ("Reject", 2)
    )
    uid_sender = ForeignKey(User, on_delete=CASCADE, related_name='request_sender')
    uid_receiver = ForeignKey(User, on_delete=CASCADE, related_name='request_receiver')
    status = IntegerField(choices=Status, null=False, default=1)
    request_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uid_sender.username

    def accept(self):
        """"
        Accept a friend request
        update friends list for both sender and receiver
        """
        receiver_friend_list = Friend.objects.get(user=self.uid_receiver)  # query receiver's friend list
        if receiver_friend_list:  # if receiver friend list exists
            receiver_friend_list.add_friend(self.uid_sender)  # add sender to receiver's friend list
            sender_friend_list = Friend.objects.get(user=self.uid_sender)  # query sender's friend list
            if sender_friend_list:  # if that friend exists
                sender_friend_list.add_friend(self.uid_receiver)  # add receiver to sender's friend list
                self.status = 0  # update F.R. status to 0 (aka accepted)
                self.save()
                return True

    def reject(self):
        """"
        Reject a friend request
        """
        self.status = 2  # update F.R. status to 2 (aka rejected)
        self.save()

    def cancel(self, sent_request):
        """"
        cancel a sent friend request
        """
        sent_request.delete()
