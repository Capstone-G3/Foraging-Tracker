from django.views import View
from django.shortcuts import render
from forage.sitemap import BaseMap

class Home_View(View):
    def __init__(self):
        self.figure = BaseMap()

    def get(self,request):
        return render(request, "index.html", {"map" : self.figure})