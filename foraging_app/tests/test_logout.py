from django.test import TestCase
from django.test import Client
from foraging_app.models.user import User
from foraging_app.models.user_profile import User_Profile


class Logout(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(id=000, username='BobFindings', password='1234')
        self.user1.save()
        self.user_profile1 = User_Profile.objects.create(
            first_name='Bob', last_name='S',
            email='Bob@gmail.com', home_address='234 N Ave',
            phone='414-123-4567', user_id=self.user1
        )
        self.user_profile1.save()

    #   **********UN-COMMENT OUT REST UPON LOGIN IMPLEMENTATION**********
    #   test a logged-in user is able to successfully log out
    def test_isLoggedOut(self):
        self.client.login(username='BobFindings', password='1234')
        # self.client.post('/login/', {'username': 'BobFindings', 'password': '1234'})

        # self.assertTrue('_auth_user_id' in self.client.session)
        self.client.post('logout/')
        self.assertFalse('_auth_user_id' in self.client.session)

    #   **********UN-COMMENT OUT REST UPON LOGIN IMPLEMENTATION**********
    # test user is redirected back to home page if they log out
    def test_logged_out_from_other_pages(self):
        self.client.login(username='BobFindings', passowrd='1234')
        # self.assertTrue(self.client.session.get('_auth_user_id'))
        response = self.client.post('logout/')
        # self.assertRedirects(response, '')
