from django.views import View
from django.shortcuts import render
from foraging_app.models.user import User
from foraging_app.models.user import User_Profile

class User_View(View):

    def get(self, request):
        #TODO: When adding in ability to view other users, check if user exists, pass in empty models if not.
        profile = User_Profile.objects.get(pk=request.user.id)
        #TODO: Originally I was going to check if this is null, but it seems the property doesn't exist currently, change this when it is added.
        if (not request.user.profile_image):
            profilePhoto = "/static/css/images/user_logo.png"
        else:
            profilePhoto = request.user.profile_image.url
        return render(request, "user.html", {"user": request.user, "userProfile": profile, "profilePhoto": profilePhoto})