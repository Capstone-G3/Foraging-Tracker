from django.views import View
from django.shortcuts import render
from forage.sitemap import DesktopMap, BaseMap

class Home_View(View):
    def __init__(self):
        self.figure = DesktopMap().compile_figure()

    def get(self,request):
        username = request.user.username if request.user.is_authenticated else "Log In"
        return render(request, "index.html", {"map" : self.figure , "username" : username})

class About_Us_View(View):
    def get(self, request):
        return render(request, "about_us.html", {})