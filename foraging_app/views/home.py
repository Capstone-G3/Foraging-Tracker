from django.views import View
from django.shortcuts import render
from forage.sitemap import DesktopMap, BaseMap

class Home_View(View):
    def __init__(self):
        self.figure = DesktopMap().compile_figure()

    def get(self,request):
        if request.user.is_authenticated:
            username = request.user
            userLink = "user"
        else:
            username = "Log In"
            userLink = "login"
        return render(request, "index.html", {"map": self.figure, "username": username, "userLink": userLink})

class About_Us_View(View):
    def get(self, request):
        return render(request, "about_us.html", {})