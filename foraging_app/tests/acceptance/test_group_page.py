from django.test import TestCase, Client
from django.urls import reverse
import datetime

from foraging_app.models.group import Group, User_Group
from foraging_app.models.user import User, User_Profile
from foraging_app.models.marker import Marker
from django.contrib.auth.hashers import make_password
from django.contrib.messages import get_messages


class GroupPageTest(TestCase):



    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.group_url = reverse('group')
        self.home_url = reverse('home')

        self.user = User.objects.create(
            username='test',
            password=make_password('testpassword'),
            rating=0,
            profile_image='path/to/image.jpg',
            first_name='test',
            last_name='User',
            email='testuser@example.com'
        )
        self.user_profile = User_Profile.objects.create(home_address='1111 N test st',
                                                        phone='5555555555',
                                                        gender=1,
                                                        user_id=self.user)
        self.client.post(self.login_url, {'username': self.user.username, 'password': self.user.password})



    def handleSetup(self, isAdmin, isPrivate):
        if isAdmin and isPrivate:
            group = Group.objects.create(name='testGroup', category='Private',
                                         description='Hello there!', user_admin=self.user)
            return group
        elif isAdmin and not isPrivate:
            group = Group.objects.create(name='testGroup', category='Public',
                                         description='Hello there!', user_admin=self.user)
            return group
        elif not isAdmin and isPrivate:
            adminUser = User.objects.create(username='testAdmin',
                                            password=make_password('testpassword'),
                                            rating=0,
                                            profile_image='path/to/image.jpg',
                                            first_name='admin',
                                            last_name='User',
                                            email='adminuser@example.com')

            group = Group.objects.create(name='testGroup', category='Private',
                                         description='Hello there!', user_admin=adminUser)
            return group
        else:
            adminUser = User.objects.create(username='testAdmin',
                                            password=make_password('testpassword'),
                                            rating=0,
                                            profile_image='path/to/image.jpg',
                                            first_name='admin',
                                            last_name='User',
                                            email='adminuser@example.com')

            group = Group.objects.create(name='testGroup', category='Public',
                                         description='Hello there!', user_admin=adminUser)
            return group






    def test_group_view_get(self):
        admin = True
        public = True

        group = self.handleSetup(admin, public)

        response = self.client.get(self.group_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'group.html')

    def test_group_join_private(self):
        admin = False
        private = True

        group = self.handleSetup(admin, private)

        response = self.client.post(reverse('join_group', args=[group.id]))
        self.assertEqual(response.status_code, 200) #302?
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Request to join " + group.name + " successfully sent")

    def test_group_join_public(self):
        admin = False
        public = True

        group = self.handleSetup(admin, public)
        self.user_group = User_Group.objects.create(user_id=group.user_admin, group_id=group)

        response = self.client.post(reverse('join_group', args=[group.id]))
        self.assertEqual(response.status_code, 200)  # 302?

        self.assertTrue(self.user_group.existInGroup(self.user, group))

    def test_group_view_profile(self):
        admin = False
        public = True
        group = self.handleSetup(admin, public)
        member = User.objects.create(
            username='tempMember',
            password=make_password('testpassword2'),
            rating=0,
            profile_image='path/to/image.jpg',
            first_name='temp',
            last_name='Member',
            email='tempuser@example.com'
        )
        User_Group.objects.create(user_id=member, group=group)
        response = self.client.get(reverse('view_profile', args=[member.id]))
        self.assertRedirects(response, reverse('profile', args=[member.id])) #need for args?

    def test_group_view_post(self):
        admin = False
        public = True
        group = self.handleSetup(admin, public)
        member = User.objects.create(
            username='tempMember',
            password=make_password('testpassword2'),
            rating=0,
            profile_image='path/to/image.jpg',
            first_name='temp',
            last_name='Member',
            email='tempuser@example.com'
        )
        User_Group.objects.create(user_id=member, group=group)
        marker = Marker.objects.create(title='Test Marker',
                                       latitude=1,
                                       longitude=1,
                                       is_private=False,
                                       owner=member)
        response = self.client.get(reverse('view_marker', args=[marker.id]))
        self.assertRedirects(response, reverse('marker', args=[marker.id])) #need for args?

    def test_group_to_home(self):
        admin = False
        public = True
        group = self.handleSetup(admin, public)
        response = self.client.get(reverse('home', args=[group.id]))
        self.assertRedirects(response, self.home_url)

    def test_group_to_your_profile(self):
        admin = False
        public = True
        group = self.handleSetup(admin, public)
        response = self.client.get(reverse('to_your_profile', args=[group.id]))
        self.assertRedirects(response, reverse('profile', args=[self.user.id]))

    def test_group_to_main_feed(self):
        admin = False
        public = True
        group = self.handleSetup(admin, public)
        response = self.client.get(reverse('to_main_feed', args=[group.id]))
        self.assertRedirects(response, reverse('main_feed'))

    def test_group_edit_name(self):
        admin = True
        public = True
        group = self.handleSetup(admin, public)
        response = self.client.post(reverse('edit_group', args=[group.id]),
                                    {'name': 'name change',
                                     'category': 'Public',
                                     'description': 'Hello there!'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(group.name == 'name change')

    def test_group_edit_category(self):
        admin = True
        public = True
        group = self.handleSetup(admin, public)
        response = self.client.post(reverse('edit_group', args=[group.id]),
                                    {'name': 'testGroup',
                                     'category': 'Private',
                                     'description': 'Hello there!'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(group.category == 'Private')

    def test_group_edit_description(self):
        admin = True
        public = True
        group = self.handleSetup(admin, public)
        response = self.client.post(reverse('edit_group', args=[group.id]),
                                    {'name': 'testGroup',
                                     'category': 'Public',
                                     'description': 'General Kenobi!'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(group.description == 'General Kenobi!')


    def test_group_remove_member(self):
        admin = True
        public = True

        group = self.handleSetup(admin, public)
        member = User.objects.create(
            username='tempMember',
            password=make_password('testpassword2'),
            rating=0,
            profile_image='path/to/image.jpg',
            first_name='temp',
            last_name='Member',
            email='tempuser@example.com'
        )
        self.user_group = User_Group.objects.create(user_id=member, group=group)

        response = self.client.post(reverse('remove_member', args=[member.id]))
        self.assertEqual(response.status_code, 200)  # 302?

        self.assertFalse(self.user_group.existInGroup(member, group))












