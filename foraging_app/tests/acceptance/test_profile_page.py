from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from foraging_app.models import User, Group, Marker, Species
from foraging_app.models.group import User_Group
from foraging_app.models.marker import User_Marker
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
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.profile_url = reverse('profile')
        self.client.post(self.login_url, {'username': self.user.username, 'password': '12345'})
        self.species1 = Species.objects.create(id=123, name='Species 1', category='fruit'
                                               , scope='testscope', description='Found berry', image='/testImagePath')
        self.marker1 = Marker.objects.create(id=0000, title='Lion''s mane', latitude=43.07866235729638,
                                             longitude=-87.881974725981,
                                             is_private=False, species=self.species1, owner=self.user)
        self.user_marker1 = User_Marker.objects.create(user_id=self.user, marker_id=self.marker1,
                                                       saved_date=datetime.now())
        self.group1 = Group.objects.create(name='Group 1')
        self.user_group1 = User_Group.objects.create(group=self.group1, user=self.user)

    # test user can reach their profile page
    def test_can_reach_profile_page(self):
        response = self.client.post(reverse('profile', args=self.user_profile.id))
        self.assertEqual(response.status_code, 200)

    #   test user can edit their profile page
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

    #   test user can manage(accept/remove) their friends on their profile page
    # def test_profile_manage_friends(self):
    #     user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='0000', )
    #     user3 = User.objects.create_user(username='user3', email='user3@gmail.com', password='1111', )
    #     #TO DO*************** test will run after friend/friendship implementation
    #     friendship = Friend.objects.create(user_a=self.user, user_br=user2, friend_since=datetime.now())
    #     friend_request = Friend_Request.objects.create(uid_sender=user3, uiweweweweed_receiver=self.user, status=1,
    #                                                    request_date=datetime.now())

        # self.client.post(reverse('profile', args=self.user_profile.id))
        # response = self.client.post(reverse('friends'))
        # self.assertEqual(response.status_code, 200)
        # # TO DO*************** figure out if the view for managing friends would be a single view that handles
        # # accepting and rejecting request
        # self.client.post(reverse('manage_friend_request', args=user3), {'friend_request': 'accept'})
        # self.assertEqual(friend_request.status, 1)
        #
        # response = self.client.post(reverse('manage_friends', args=user3), {'remove_friend': True})
        # self.assertEqual(response.status_code, 200)

    #   test user can view their posts on their profile page
    def test_see_own_posts(self):
        response = self.client.get(reverse('profile', args=self.user.id))
        self.assertContains(response,
                            self.user_marker1.marker_id)  # double check if the marker id is way to recognize the
        # post on page

    #   test user can delete their posts from their profile page
    def test_delete_my_posts(self):
        self.client.get(reverse('profile', args=self.user.id))
        response = self.client.post(reverse('delete_marker', args=self.marker1.id))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('profile', args=self.user.id))
        self.assertNotContains(response, self.user_marker1.marker_id)

    #   test user can create posts from their profile
    def test_create_new_post(self):
        marker = {'title': 'test marker', 'latitude': 43.07866235729638, 'longitude': -87.881974725981,
                  'is_private': False, 'species': self.species1}
        response = self.client.post(reverse('create_marker'), marker)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('profile', args=self.user.id))
        self.assertContains(response, 'test marker')

    #   test user can create a group from their profile
    def test_create_group(self):
        self.client.post(reverse('profile', args=self.user_profile.id))
        self.client.post(reverse('create_group'))
        group = {'name': 'test group', 'description': 'group description', 'category': 'mushrooms', 'is_private': False}
        response = self.client.post(reverse('create_group'), {group})
        self.client.post(reverse('profile', args=self.user_profile.id))
        self.assertContains(response, 'test group')

    #   test user can view groups from their profile
    def test_view_groups(self):
        self.client.post(reverse('profile', args=self.user_profile.id))
        response = self.client.post(reverse('profile', args=self.user.id))
        self.assertContains(response, self.group1.id)

    #   test user can reach edit their account
    def test_adjust_profile_settings(self):
        self.client.post(reverse('profile', args=self.user_profile.id))
        self.client.post(reverse('edit_account', args=self.user.id),
                         {'email': 'newtest@gmail.com', 'password': '32454'})
        self.assertEqual(self.user.email, 'newtest@gmail.com')
        self.assertEqual(self.user.password, '32454')

    #   test user can delete their account
    def test_delete_profile(self):
        self.client.post(reverse('profile', args=self.user_profile.id))
        response = self.client.post(reverse('delete_account', args=self.user.id))
        self.assertRedirects(response, reverse('home'))

        user = User.objects.get(self.user.id)
        self.assertIsNone(user)

    #   test user can view other's posts from their profiles
    def test_can_view_others_posts_on_their_profiles(self):
        user2 = User.objects.create_user(username='test2', email='test2@gmail.com', password='1111',
                                         profile_image='test.png')
        User_Profile.objects.create(home_address='123 S Ave', phone='123 456 789', gender=1,
                                    user_id=user2)
        marker2 = Marker.objects.create(id=111, title='Lion''s mane', latitude=43.07866235729638,
                                        longitude=-87.881974725981,
                                        is_private=False, species=self.species1, owner=user2)
        self.user_marker2 = User_Marker.objects.create(user_id=user2, marker_id=marker2,
                                                       saved_date=datetime.now())
        response = self.client.post(reverse('profile', args=user2.id))
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, 'Lion''s mane')

    #   test user can view their badge level on their profile
    def test_can_view_badge_level(self):
        response = self.client.post(reverse('profile', args=self.user.id))
        self.assertContains(response, 'Bronze')
