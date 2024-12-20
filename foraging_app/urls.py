"""
URL configuration for foraging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from foraging_app.views.group_view import Group_View, Create_Group_View, Group_Nav_View, Group_Edit_View, \
    Group_Delete_View, AddCommentGroupView, RemoveMemberGroupView, Request_Private_Group_Join_View
from foraging_app.views.home import Home_View, About_Us_View, Feed_View, AddCommentView, SingleMarkerView, \
    ShareMarkerView, DeleteCommentView, notification_count
from foraging_app.views.login import Login_View
from foraging_app.views.logout import Logout_View
from foraging_app.views.registration import Register_View
from foraging_app.views.user import User_View, AddCommentUserView
from foraging_app.views.marker import Marker_Create_View, Marker_Edit_View, Marker_Home_View, Marker_Delete_View, Marker_Details_View
from foraging_app.views.edit_profile import EditProfileView
from foraging_app.views.delete_account import DeleteUserView
from foraging_app.views.categories import CategoriesView, CategoryDetailView
from foraging_app.views.like_view import LikeMarkerView
from foraging_app.views.leaderboard import LeaderboardView
from foraging_app.views.notification_view import NotificationListView, mark_notifications_as_read, mark_notification_as_read
from django.conf import settings
from django.conf.urls.static import static
from django.core.mail import send_mail
from foraging_app.views.friends import AcceptFriendRequestView, RejectFriendRequestView, \
    FriendsView, RemoveFriendView, CancelFriendRequestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home_View.as_view(), name='home'),

    #Login urls
    path('login/', Login_View.as_view(), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html',),name='password_reset_complete'),
    path('register/', Register_View.as_view(), name = 'register'),

    #User urls
    path('user/<int:userId>/', User_View.as_view(), name = 'user'),
    path('add_comment/<int:marker_id>/<int:user_id>', AddCommentUserView.as_view(), name='add_comment'),
    path('about_us/', About_Us_View.as_view(), name='about_us'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/<str:category>/', CategoryDetailView.as_view(), name='category_detail'),
    path('group/<int:groupID>', Group_View.as_view(), name='group'),
    path('group_edit/<int:groupID>', Group_Edit_View.as_view(), name='group_edit'),
    path('group_nav/', Group_Nav_View.as_view(), name='group_nav'),
    path('group_delete_confirmation/<int:groupID>', Group_Delete_View.as_view(), name='group_delete_confirmation'),
    path('create_group/', Create_Group_View.as_view(), name='create_group'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/<str:category>/', CategoryDetailView.as_view(), name='category_detail'),

    #Logout url
    path('logout/', Logout_View.as_view(), name="logout"),
    # Marker urls
    path('markers/', Marker_Home_View.as_view(), name='home_marker'),
    path('marker/create', Marker_Create_View.as_view(), name="create_marker"),
    path('marker/<int:marker_id>', Marker_Details_View.as_view(), name='info_marker'),
    path('marker/<int:marker_id>/edit', Marker_Edit_View.as_view(), name='edit_marker'),
    path('marker/<int:marker_id>/delete', Marker_Delete_View.as_view(), name='delete_marker'),
    #edit profile url
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    #delete acc view
    path('delete/', DeleteUserView.as_view(), name='delete'),
    path('feed/', Feed_View.as_view(), name='feed'),
    path('like/<int:marker_id>/', LikeMarkerView.as_view(), name='like_marker'),
    path('add_comment_group/<int:marker_id>/<int:groupID>/', AddCommentGroupView.as_view(), name='add_comment_group'),
    path('remove_member_group/<int:groupID>/<int:userID>/', RemoveMemberGroupView.as_view(), name='remove_member_group'),
    path('request_private_group_join_response/<int:groupID>/<int:newMemberID>/', Request_Private_Group_Join_View.as_view(), name='request_private_group_join_response'),
    path('add_comment/<int:marker_id>/', AddCommentView.as_view(), name='add_comment'),
    path('delete_comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('map/marker/<int:marker_id>/', SingleMarkerView.as_view(), name='single_marker'),

    #friend urls
    path('friends/', FriendsView.as_view(), name='friends'),
    path('send_friend_request/<int:user_id>/', FriendsView.as_view(), name='send_friend_request'),
    path('accept_friend_request/<int:user_id>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('reject_friend_request/<int:user_id>/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('remove_friend/<int:user_id>/', RemoveFriendView.as_view(), name='remove_friend'),
    path('share_marker/', ShareMarkerView.as_view(), name='share_marker'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('api/notifications/count/', notification_count, name='notification_count'),
    path('notifications/mark_as_read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    path('notifications/mark-as-read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('cancel_friend_request/<int:user_id>/', CancelFriendRequestView.as_view(), name='cancel_friend_request'),
]

# Remove for Production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
