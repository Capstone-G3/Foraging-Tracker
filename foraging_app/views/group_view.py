from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from oauthlib.openid.connect.core.exceptions import LoginRequired

from foraging_app.forms.group import GroupCreateForm
from foraging_app.models.group import Group, User_Group
from foraging_app.forms import group, CommentForm
from foraging_app.models.user import User
from django.contrib.auth.hashers import make_password
from foraging_app.models import Marker


class Group_View(LoginRequiredMixin,View):
    login_url = '/login/'

    def rankingSort(self, member):
        return member.rating

    def get(self, request, groupID):
        thisGroup = Group.objects.get(id=groupID)
        members = []
        markers = []
        inGroup = False

        if thisGroup is not None:
            members = User_Group.getGroupMembers(None, thisGroup)
            members.sort(key=self.rankingSort, reverse=True)
            markers = User_Group.getGroupMarkers(None, thisGroup)
            for x in members:
                if x.id == request.user.id:
                    inGroup = True
        return render(request, "groups/group.html", {'thisGroup': thisGroup,
                                              'members': members,
                                              'markers': markers,
                                              'form': CommentForm(),
                                              'inGroup': inGroup})

    def post(self, request, groupID):
        thisGroup = Group.objects.get(id=groupID)
        if thisGroup.isPrivate:
            # TODO: set up request system for private groups
            messages.success(request, "Requested to join " + thisGroup.name)
            return redirect('group', groupID)
        else:
            User_Group.objects.create(group_id=thisGroup, user_id=request.user)
            messages.success(request, "Successfully joined " + thisGroup.name)
            return redirect('group', groupID)



class AddCommentGroupView(View):
    def post(self, request, marker_id, groupID):
        marker = Marker.objects.get(id=marker_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.marker = marker
            comment.user = request.user
            comment.save()
        return redirect('group', groupID)


class Create_Group_View(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self, request):
        form = GroupCreateForm()
        return render(request, "groups/create_group.html", {'form': form})

    def post(self, request):
        form = GroupCreateForm(request.POST)
        status = 400
        if form.is_valid():
            data = form.cleaned_data
            group_create = Group.objects.create(**data, user_admin=request.user)
            User_Group.objects.create(group_id=group_create, user_id=request.user)
            if group_create is not None:
                messages.success(request,"Group creation complete.")
                return redirect('group', group_create.id)
            else:
                messages.error(request, "Group failed to create.")

        return render(request, "groups/create_group.html", {'form': GroupCreateForm()}, status=status)


class Group_Nav_View(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self, request):
        allGroups = Group.objects.order_by("name")
        return render(request, "groups/group_nav.html", {'allGroups': allGroups})




class Group_Edit_View(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self, request, groupID):
        thisGroup = Group.objects.get(id=groupID)
        return render(request, "groups/group_edit.html", {'thisGroup': thisGroup})


    def post(self, request, groupID):
        thisGroup = Group.objects.get(id=groupID)

        thisGroup.name = request.POST['name']
        thisGroup.description = request.POST['description']
        if request.POST['isPrivate'] == 'Public':
            thisGroup.isPrivate = False
        else:
            thisGroup.isPrivate = True
        thisGroup.save()

        return redirect('group', thisGroup.id)


class Group_Delete_View(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self, request, groupID):
        thisGroup = Group.objects.get(id=groupID)
        return render(request, "groups/group_delete_confirmation.html", {'thisGroup': thisGroup})

    def post(self, request, groupID):
        thisGroup = Group.objects.get(id=groupID)
        thisGroup.delete()
        messages.success(request, "Group deletion complete.")
        return redirect('group_nav')



