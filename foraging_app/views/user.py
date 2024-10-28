from django.views import View
from django.shortcuts import render
from foraging_app.models.user import User
from foraging_app.models.user import User_Profile

class User_View(View):

    def get(self, request, userId = None):
        isPersonalAccount = False
        user = None
        if (userId == None):
            userId = request.user.id
            user = request.user
            isPersonalAccount = True
        else:
            try:
                user = User.objects.get(id=userId)
            except User.DoesNotExist:
                user = None
            isPersonalAccount = False
        
        try:
            userProfile = User_Profile.objects.get(user_id=userId)
        except User_Profile.DoesNotExist:
            userProfile = None

        if (user == None or not user.profile_image):
            profilePhoto = "/static/css/images/user_logo.png"
        else:
            profilePhoto = user.profile_image.url
        return render(request, "user.html", {"userModel": user, "userProfile": userProfile, "profilePhoto": profilePhoto, "isPersonalAccount": isPersonalAccount})