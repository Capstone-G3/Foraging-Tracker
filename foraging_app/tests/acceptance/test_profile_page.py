from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from foraging_app.models import User, Group
from foraging_app.models.user import User_Profile
import os
import tempfile


class ProfilePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', email='test@gmail.com', password='12345',
                                             profile_image='test.png')
        self.user_profile = User_Profile.objects.create(home_address='123 S Ave', phone='123 456 789', gender=1,
                                                        user_id=self.user)
        self.user.friend
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.profile_url = reverse('profile')
        self.client.post(self.login_url, {'username': self.user.username, 'password': '12345'})
        # self.assertTrue(self.client.login(username='test', password='<PASSWORD>'))

    def test_can_reach_profile_page(self):
        response = self.client.post(reverse('profile', args=self.user_profile.id))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_page(self):
        self.client.post(reverse('profile', args=self.user_profile.id))
        testImagePath = tempfile.NamedTemporaryFile(suffix=".png").name
        # 1x1 black pixel image
        with open(testImagePath, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n'
                    b'\x00\x00\x00\rIHDR'
                    b'\x00\x00\x00\x01'
                    b'\x00\x00\x00\x01'
                    b'\x08\x02\x00\x00\x00'
                    b'\xd2\xc5\xf5\x3d'
                    b'\x00\x00\x00\x0bIDAT'
                    b'x\x9c'
                    b'\x01\x00\x00\x00\x01'
                    b'\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00')
        response = self.client.post(reverse('profile', args=self.user.id))
        self.assertContains('Edit', response)

        response = self.client.post(reverse('edit_profile', args=self.user.id),
                                    {'first name': 'Bob',
                                     'last name': 'S',
                                     'bio': 'this is my bio',
                                     'post privacy': True, 'profile picture': testImagePath
                                     })
        self.assertEqual(response.status_code, 200)
        os.remove(testImagePath)

    def test_profile_manage_friends(self):
        user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='0000', )
        user3 = User.objects.create_user(username='user3', email='user3@gmail.com', password='1111', )
        friendship = Friend.objects.create(user_a=self.user, user_br=user2, friend_since=datetime.now())
        friend_request = Friend_Request.objects.create(uid_sender=user3, uiweweweweed_receiver=self.user, status=1,
                                                       request_date=datetime.now())

        self.client.post(reverse('profile', args=self.user_profile.id))
        response = self.client.post(reverse('friends'))
        self.assertEqual(response.status_code, 200)
        #TODO figure out if the view for managing friends would be a single view that handles accepting and rejecting request
        self.client.post(reverse('manage_friend_request', args=user3), {'friend_request': 'accept'})
        self.assertEqual(friend_request.status, 1)
        # add a test case to see friends list

    def test_see_own_posts(self):
        pass

    def test_delete_my_posts(self):
        pass

    def test_create_new_post(self):
        pass

    def test_view_groups(self):
        pass

    def test_adjust_profile_settings(self):
        pass

    def test_delete_account(self):
        pass

    def test_can_view_others_posts_on_their_profiles(self):
        pass

    def test_can_view_others_friends_list(self):
        pass

    def test_can_view_badge_level(self):
        pass

    def test_can_navigate_to_other_pages(self):
        pass

# class GroupsPageTest(TestCase):
#     def setup(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='test', email='test@gmail.com', password='12345',
#                                              profile_image='test.png')
#         self.user_profile = User_Profile.objects.create(home_address='123 S Ave', phone='123 456 789', gender=1,
#                                                         user_id=self.user)
#         self.login_url = reverse('login')
#         self.home_url = reverse('home')
#         self.client.post(self.login_url, {'username': self.user.username, 'password': '12345'})
#
#     def handleSetup(self, isAdmin):
#         # group = Group.objects.create(name='test', description='test')
#         if isAdmin:
#
#             group = Group.objects.create(name='test_group', description='test', user_admin=self.user)
#             return group
#
#         else:
#             user2 = User.objects.create_user(username='test2', email='test2@gmail.com', password='1111',
#                                              profile_image='test.png')
#             group = Group.objects.create(name='test_group', description='test', user_admin=user2)
#             return group
#
#     def test_request_to_join(self):
#         admin = False
#         group = self.handleSetup(admin)
#
#         response = self.client.post(reverse('join_group', args=[group.id]))
#         self.assertTrue(response.status_code == 200)
#
#     def test_can_edit_groups(self):
#         admin = True
#         group = self.handleSetup(admin)
#         # .... make test for this case
#
#     def test_get
