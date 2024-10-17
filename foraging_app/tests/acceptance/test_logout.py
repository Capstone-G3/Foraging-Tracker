from django.test import TestCase
from django.test import Client
from django.urls import reverse
from foraging_app.models.user import User
from foraging_app.models.user import User_Profile


class Logout(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(id=000, username='BobFindings', password='1234')
        self.user_profile = User_Profile.objects.create(home_address='123 S St', phone='414-123-4567', gender=2, user_id=self.user)
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.logout_url = reverse('logout')

    #   test logged-in user can access logout view and log out
    def test_isLoggedOut(self):
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': self.user.password})
        self.assertRedirects(response, '/login/')
        response = self.client.post(self.logout_url)
        self.assertFalse('_auth_user_id' in self.client.session)

    # test user is redirected back to home page if they log out
    def test_logged_out_from_other_pages(self):
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': self.user.password})
        self.assertRedirects(response, '/login/')
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, self.home_url)
