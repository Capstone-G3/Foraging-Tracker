from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from foraging_app.models.user import User
from foraging_app.models.friend import Friend, Friend_Request
from foraging_app.models.notification import Notification


class FriendsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # get user object
        try:
            user = request.user
        except User.DoesNotExist:
            user = None
        # query list of friend request sent by user
        try:
            sent_friend_requests = Friend_Request.objects.filter(uid_sender=user, status=1)
        except Friend_Request.DoesNotExist:
            sent_friend_requests = None
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
                      {'friends': friends,
                       'received_requests': received_friend_requests,
                       'sent_friend_request': sent_friend_requests})

    def post(self, request, user_id):
        user_sender = request.user
        user_to_add = User.objects.get(id=user_id)

        if not Friend_Request.objects.filter(uid_receiver=user_to_add, uid_sender=user_sender):
            Friend_Request.objects.create(uid_receiver=user_to_add, uid_sender=user_sender)
        Notification.objects.create(
            user=user_to_add,
            message=f'{user_sender.username} sent you a friend request.'
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'friends'))


class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user = request.user
        user_to_add = User.objects.get(id=user_id)
        Friend_Request.objects.get(uid_receiver=user, uid_sender=user_to_add).accept()
        Notification.objects.create(
            user=user_to_add,
            message=f'{user.username} accepted your friend request.'
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'friends'))


class RejectFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user = request.user
        user_to_reject = User.objects.get(id=user_id)
        Friend_Request.objects.get(uid_receiver=user, uid_sender=user_to_reject).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'friends'))


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user = request.user
        user_to_remove = User.objects.get(id=user_id)
        friend_doing_removing = Friend.objects.get(user=user)
        # friend_to_remove = Friend.objects.get(user=user_to_remove)
        Friend.unfriend(friend_doing_removing, user_to_remove)

        #   handle removing friend_request from no longer active friend  relationship
        try:
            friend_req1 = Friend_Request.objects.get(uid_receiver=user, uid_sender=user_to_remove)
        except Friend_Request.DoesNotExist:
            friend_req1 = None
        try:
            friend_req2 = Friend_Request.objects.get(uid_receiver=user_to_remove, uid_sender=user)
        except Friend_Request.DoesNotExist:
            friend_req2 = None
        if friend_req1:
            friend_req1.delete()
        if friend_req2:
            friend_req2.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'friends'))


class CancelFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        sender = request.user
        receiver = User.objects.get(id=user_id)
        sent_friend_request = Friend_Request.objects.get(uid_receiver=receiver, uid_sender=sender)
        Friend_Request.cancel(sender, sent_friend_request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'friends'))
