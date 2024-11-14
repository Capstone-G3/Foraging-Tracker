from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from oauthlib.openid.connect.core.exceptions import LoginRequired
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

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
            text_content = render_to_string("emails/request_private_join.txt")
            html_content = render_to_string("emails/request_private_group_join.html",
                                            context={'thisGroup': thisGroup, 'thisUser': request.user})
            msg = EmailMultiAlternatives("Request to Join Your Group!",
                                         text_content,
                                         "<EMAIL>",
                                         [thisGroup.user_admin.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, "Requested to join " + thisGroup.name)
            return redirect('group', groupID)
        else:
            User_Group.objects.create(group_id=thisGroup, user_id=request.user)
            messages.success(request, "Successfully joined " + thisGroup.name)
            return redirect('group', groupID)

class Request_Private_Group_Join_View(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, groupID, newMemberID):
        thisGroup = Group.objects.get(id=groupID)
        newMember = User.objects.get(id=newMemberID)
        return render(request, 'groups/request_private_group_join_response.html',
                      {'thisGroup': thisGroup, 'newMember': newMember})

    def post(self, request, groupID, newMemberID):
        thisGroup = Group.objects.get(id=groupID)
        newMember = User.objects.get(id=newMemberID)
        User_Group.objects.create(group_id=thisGroup, user_id=newMember)
        send_mail("Accepted into " + thisGroup.name,
                  "Yippee!  You were accepted into the group " + thisGroup.name,
                  "<EMAIL>",
                  [newMember.email])
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

class RemoveMemberGroupView(View):
    def post(self, request, groupID, userID):
        thisGroup = Group.objects.get(id=groupID)
        thisUser = User.objects.get(id=userID)
        thisUserGroup = User_Group.objects.get(group_id=thisGroup, user_id=thisUser)
        thisUserGroup.delete()
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



