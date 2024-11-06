from django.views import View
from django.shortcuts import render
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

        return render(request, "user.html", {'form': CommentForm(), "userModel": user, "userProfile": userProfile, "profilePhoto": profilePhoto, "markers": markers, "isPersonalAccount": isPersonalAccount})