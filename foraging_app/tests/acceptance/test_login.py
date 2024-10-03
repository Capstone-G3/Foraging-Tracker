from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from foraging_app.models.user import User, User_Profile
from django.contrib.auth.hashers import make_password
from django.contrib.messages import get_messages
from foraging_app.views.login import Login_View
from django.contrib.messages.storage.fallback import FallbackStorage

class LoginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.user = User.objects.create(
            username='testuser',
            password=make_password('testpassword'),
            rating=0,
            profile_image='path/to/image.jpg',
            first_name='Test',
            last_name='User',
            email='testuser@example.com'
        )
        self.user_profile = User_Profile.objects.create(

            home_address='123 Test St',
            phone='1234567890',
            gender= 2,
            user_id=self.user
        )

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_success(self):
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': 'testpassword'})
        print(self.user.password)
        print(response.content)
        self.assertRedirects(response, self.home_url)

    def test_login_view_post_failure(self):
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': 'wrongpassword'})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_login_view_post_no_username(self):
        response = self.client.post(self.login_url, {'password': 'testpassword'})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_no_password(self):
        response = self.client.post(self.login_url, {'username': self.user.username})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_empty_username(self):
        response = self.client.post(self.login_url, {'username': '', 'password': 'testpassword'})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_empty_password(self):
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': ''})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_invalid_username(self):
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'testpassword'})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_invalid_password(self):
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': 'invalidpassword'})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_case_sensitive_username(self):
        response = self.client.post(self.login_url, {'username': self.user.username.upper(), 'password': 'testpassword'})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_case_sensitive_password(self):
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': 'TESTPASSWORD'})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_special_characters_username(self):
        special_username = 'testuser!@#'
        User.objects.create(username=special_username, password=make_password('testpassword'))
        response = self.client.post(self.login_url, {'username': special_username, 'password': 'testpassword'})
        self.assertRedirects(response, self.home_url)

    def test_login_view_post_special_characters_password(self):
        special_password = 'testpassword!@#'
        User.objects.create(username='testuser2', password=make_password(special_password))
        response = self.client.post(self.login_url, {'username': 'testuser2', 'password': special_password})
        self.assertRedirects(response, self.home_url)

    def test_login_view_post_sql_injection(self):
        response = self.client.post(self.login_url, {'username': "' OR 1=1 --", 'password': 'testpassword'})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_xss_attack(self):
        response = self.client.post(self.login_url, {'username': '<script>alert(1)</script>', 'password': 'testpassword'})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_long_username(self):
        long_username = 'a' * 256
        response = self.client.post(self.login_url, {'username': long_username, 'password': 'testpassword'})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_long_password(self):
        long_password = 'a' * 256
        response = self.client.post(self.login_url, {'username': self.user.username, 'password': long_password})
        self.assertRedirects(response, self.login_url)

    def test_login_view_post_unicode_username(self):
        unicode_username = '测试用户'
        User.objects.create(username=unicode_username, password=make_password('testpassword'))
        response = self.client.post(self.login_url, {'username': unicode_username, 'password': 'testpassword'})
        self.assertRedirects(response, self.home_url)

    def test_login_view_post_unicode_password(self):
        unicode_password = '测试密码'
        User.objects.create(username='testuser3', password=make_password(unicode_password))
        response = self.client.post(self.login_url, {'username': 'testuser3', 'password': unicode_password})
        self.assertRedirects(response, self.home_url)