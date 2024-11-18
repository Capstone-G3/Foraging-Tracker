from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from foraging_app.models.user import User
from foraging_app.models.friend import Friend, Friend_Request


class FriendsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # get user object
        try:
            user = request.user
        except User.DoesNotExist:
            user = None

        # querying users not including user's the user has sent a friend request to/ received a friend request from
        try:
            all_users = []
            unfiltered_users = User.objects.all().exclude(id=user.id)
            for u in unfiltered_users:
                if not Friend_Request.objects.filter(uid_sender=u, uid_receiver=user):
                    if not Friend_Request.objects.filter(uid_receiver=u, uid_sender=user):
                        all_users.append(u)
        except User.DoesNotExist:
            all_users = None
        # query list of user's who user has sent friend request
        try:
            sent_friend_request = Friend_Request.objects.filter(uid_sender=user, status=1)
            sent_friend_request_users = sent_friend_request.values_list('uid_receiver', flat=True)
        except Friend_Request.DoesNotExist:
            sent_friend_request_users = None
        # query friend requests received by user
        try:
            received_friend_requests = Friend_Request.objects.filter(uid_receiver=user, status=1)
        except Friend_Request.DoesNotExist:
            received_friend_requests = None
        # query user's friends list
        try:
            user_friend_list = Friend.objects.get(user=user)
            friends = user_friend_list.friends.all()
        except Friend.DoesNotExist:
            friends = None

        return render(request, 'friends.html',
                      {'all_users': all_users, 'friends': friends,
                       'received_requests': received_friend_requests,
                       'sent_friend_request_users': sent_friend_request_users})

    def post(self, request, user_id):
        user_sender = request.user
        user_to_add = User.objects.get(id=user_id)

        if not Friend_Request.objects.filter(uid_receiver=user_to_add, uid_sender=user_sender).exists():
            Friend_Request.objects.create(uid_receiver=user_to_add, uid_sender=user_sender)
        return redirect('friends')


class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user = request.user
        user_to_add = User.objects.get(id=user_id)
        Friend_Request.objects.get(uid_receiver=user, uid_sender=user_to_add).accept()
        return redirect('friends')


class RejectFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user = request.user
        user_to_reject = User.objects.get(id=user_id)
        Friend_Request.objects.get(uid_receiver=user, uid_sender=user_to_reject).reject()


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user = request.user
        user_to_remove = User.objects.get(id=user_id)
        Friend.unfriend(user_to_remove, user)

