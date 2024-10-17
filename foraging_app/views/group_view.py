from django.views import View
from django.shortcuts import render
from foraging_app.models.group import Group
from foraging_app.models.user import User
from django.contrib.auth.hashers import make_password


class Group_View(View):

    def get(self, request, thisGroup=None):
        return render(request, "group.html", {'thisGroup': thisGroup})