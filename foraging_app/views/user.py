from django.views import View
from django.shortcuts import render, redirect

from foraging_app.models.friend import Friend, Friend_Request
from foraging_app.models.user import User
from foraging_app.models.user import User_Profile
from foraging_app.forms import CommentForm
from foraging_app.models.marker import Marker

class User_View(View):

    def get(self, request, userId):
        isPersonalAccount = False
        if userId == request.user.id:
            isPersonalAccount = True

        # Attempt to get user object
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            user = None
        
        # Attempt to get user profile object
        try:
            userProfile = User_Profile.objects.get(user_id=userId)
        except User_Profile.DoesNotExist:
            userProfile = None

        # Attempt to get user profile image url
        if (user == None or not user.profile_image):
            profilePhoto = "/static/css/images/user_logo.png"
        else:
            profilePhoto = user.profile_image.url

        # Attempt to get user marker objects
        try:
            markers = Marker.objects.filter(owner=userId).filter(is_private=False).order_by('-created_date')
        except User_Profile.DoesNotExist:
            markers = None
        # Attempt to query friends then assign the count to variable friend_count
        friend_count = 0  # default friend_count value
        try:
            friends = user.friends.all()
            friend_count = friends.count()
        except Friend.DoesNotExist:
            friend_count = None
        this_user = request.user
        # query user to add
        try:
            user_to_add = User.objects.get(id=userId)
        except User.DoesNotExist:
            user_to_add = None

        is_friend = Friend.is_friend(this_user, user_to_add)

        # query list of user's who user has sent friend request
        try:
            sent_friend_request = Friend_Request.objects.filter(uid_sender=this_user, status=1)
            sent_friend_request_users = sent_friend_request.values_list('uid_receiver', flat=True)
        except Friend_Request.DoesNotExist:
            sent_friend_request_users = None
        # query friend request received by user
        try:
            received_friend_request = Friend_Request.objects.get(uid_receiver=this_user, uid_sender=userId, status=1)
        except Friend_Request.DoesNotExist:
            received_friend_request = None

        return render(request, "user.html", {
            "form": CommentForm(), 
            "userModel": user, 
            "userProfile": userProfile, 
            "profilePhoto": profilePhoto, 
            "markers": markers, 
            "isPersonalAccount": isPersonalAccount,
            "friend_count": friend_count,
            "user_to_add": user_to_add,
            "is_friend": is_friend,
            "sent_friend_request_users": sent_friend_request_users,
            "received_friend_request": received_friend_request,
            "this_user": this_user, })
    
class AddCommentUserView(View):
    def post(self, request, marker_id, user_id):
        marker = Marker.objects.get(id=marker_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.marker = marker
            comment.user = request.user
            comment.save()
        return redirect('user', userId=user_id)