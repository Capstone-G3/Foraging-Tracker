from django.views import View
from django.shortcuts import render, redirect
import sitemap
from django.contrib.auth import logout

class Home_View(View):
    def __init__(self):
        self.figure = sitemap.getDefaultMap()

    def get(self,request):
        return render(request, "index.html", {"map" : self.figure})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            if request.POST.get('logoutbutton'):
                logout(request)
                return redirect('')

