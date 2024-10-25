from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from oauthlib.openid.connect.core.exceptions import LoginRequired

from foraging_app.forms.group import GroupCreateForm
from foraging_app.models.group import Group, User_Group
from foraging_app.forms import group
from foraging_app.models.user import User
from django.contrib.auth.hashers import make_password


class Group_View(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self, request, thisGroup=None):
        # thisGroup = Group.objects.filter(name="test1")
        members = []
        markers = []
        if thisGroup is not None:
            members = User_Group.getGroupMembers(None, thisGroup)
            markers = User_Group.getGroupMarkers(None, thisGroup)

        return render(request, "group.html", {'thisGroup': thisGroup,
                                              'members': members,
                                              'markers': markers})

class Create_Group_View(LoginRequiredMixin,View):

    def get(self, request):
        form = GroupCreateForm()
        return render(request, "create_group.html", {'form': form})

    def post(self, request):
        form = GroupCreateForm(request.POST)
        status = 400
        if form.is_valid():
            data = form.cleaned_data
            group_create = Group.objects.create(**data, user_admin=request.user)
            User_Group.objects.create(group_id=group_create, user_id=request.user)
            if group_create is not None:
                messages.success(request,"Group creation complete.")
                members = []
                markers = []
                members = User_Group.getGroupMembers(None, group_create)
                markers = User_Group.getGroupMarkers(None, group_create)
                return render(request, "group.html", {'thisGroup': group_create,
                                              'members': members,
                                              'markers': markers})
            else:
                messages.error(request, "Group failed to create.")

        return render(request, "create_group.html", {'form': GroupCreateForm()}, status=status)
