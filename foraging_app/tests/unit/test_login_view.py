# This isn't necessary due to View already tested by Django but I'll leave it here.
from django.test import TestCase, RequestFactory
from django.urls import reverse
from foraging_app.models.user import User, User_Profile
from django.contrib.auth.hashers import make_password
from foraging_app.views.login import Login_View
from django.contrib.messages.storage.fallback import FallbackStorage

class LoginViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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
            gender=2,
            user_id=self.user
        )

    def add_middleware(self, request):
        # Adding session and messages middleware to the request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_login_view_get(self):
        request = self.factory.get(self.login_url)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_success(self):
        request = self.factory.post(self.login_url, {'username': self.user.username, 'password': 'testpassword'})
        request.session = self.client.session
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_failure(self):
        request = self.factory.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })

        # Adding messages middleware to the request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
        self.assertIn("Username or Password Do Not Match, Try Again...", [msg.message for msg in messages])

    def test_login_view_post_no_username(self):
        request = self.factory.post(self.login_url, {'password': 'testpassword'})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_no_password(self):
        request = self.factory.post(self.login_url, {'username': self.user.username})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_empty_username(self):
        request = self.factory.post(self.login_url, {'username': '', 'password': 'testpassword'})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_empty_password(self):
        request = self.factory.post(self.login_url, {'username': self.user.username, 'password': ''})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_invalid_username(self):
        request = self.factory.post(self.login_url, {'username': 'invaliduser', 'password': 'testpassword'})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_invalid_password(self):
        request = self.factory.post(self.login_url, {'username': self.user.username, 'password': 'invalidpassword'})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_case_sensitive_username(self):
        request = self.factory.post(self.login_url, {'username': self.user.username.upper(), 'password': 'testpassword'})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_case_sensitive_password(self):
        request = self.factory.post(self.login_url, {'username': self.user.username, 'password': 'TESTPASSWORD'})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_sql_injection(self):
        request = self.factory.post(self.login_url, {'username': "' OR 1=1 --", 'password': 'testpassword'})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_xss_attack(self):
        request = self.factory.post(self.login_url, {'username': '<script>alert(1)</script>', 'password': 'testpassword'})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_long_username(self):
        long_username = 'a' * 256
        request = self.factory.post(self.login_url, {'username': long_username, 'password': 'testpassword'})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_login_view_post_long_password(self):
        long_password = 'a' * 256
        request = self.factory.post(self.login_url, {'username': self.user.username, 'password': long_password})
        self.add_middleware(request)
        response = Login_View.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)