from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

class Login(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_profile = User_Profile.create(
            first_name='john', last_name='doe' ,
            email='test@gmail.com', home_address = '1234 pine',
            phone = '414-444-1244', gender = 1, user_id=1
        )

        full_name = f"{self.user_profile.first_name} {self.user_profile.last_name}"
        time = datetime.datetime(2024, 11, 10, 12, 12, 0, tzinfo=timezone.utc) #11/10/24 12:12:00

        self.user = User.create(
            id=1, name = full_name, badge = 0, created_date = time #,rating = ?
        )
        
    def test_GetUserByEmail(self):
        user = GetUserByEmail('test@gmail.com')
        self.assertEqual(user.first_name, 'john')

    def test_GetUserByEmail_NonExistentEmail(self):
        user = GetUserByEmail('nonexistent@example.com')
        self.assertIsNone(user)
    
    def test_GetUserByEmail_InvalidEmailFormat(self):
        user = GetUserByEmail('invalid-email')
        self.assertIsNone(user)

    def test_GetUserByEmail_EmptyEmail(self):
        user = GetUserByEmail('')
        self.assertIsNone(user)

    def test_GetUserByEmail_SpecialCharacters(self):
        user = GetUserByEmail('test!@gmail.com')
        self.assertIsNone(user)

    def test_GetUserByEmail_LeadingTrailingSpaces(self):
        user = GetUserByEmail(' test@gmail.com ')
        self.assertIsNone(user)

    def test_CanLogin(self):
        user = CanLogin(self.user_profile.email, self.user.password)
        full_name = f"{self.user_profile.first_name} {self.user_profile.last_name}"
        self.assertEqual(full_name, user.name)

    def test_CanLogin_WrongPassword(self):
        user = CanLogin(self.user_profile.email, 'wrongpassword')
        self.assertIsNone(user)

    def test_CanLogin_NonExistentEmail(self):
        user = CanLogin('nonexistent@example.com', self.user.password)
        self.assertIsNone(user)
    
    def test_CanLogin_EmptyEmail(self):
        user = CanLogin('', self.user.password)
        self.assertIsNone(user)

    def test_CanLogin_EmptyPassword(self):
        user = CanLogin(self.user_profile.email, '')
        self.assertIsNone(user)

    def test_CanLogin_EmptyEmailAndPassword(self):
        user = CanLogin('', '')
        self.assertIsNone(user)

    def test_CanLogin_InvalidEmailFormat(self):
        user = CanLogin('invalid-email', self.user.password)
        self.assertIsNone(user)
    ''''
    def test_login_success(self):
        response = self.client.post(reverse('login'), {
               'email' : 'test@gmail.com',
               'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
              'email' : 'test@gmail.com',
              'password' : 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_invalid_email(self):
          response = self.client.post(reverse('login'), {
                'email' : 'wrong@gmail.com',
                'password' : 'testpassword'
          })
          self.assertEqual(response.status_code, 200)
          self.assertFalse(response.content['user'].is_authenticated)

    def test_email_format(self):
          response = self.client.post(reverse('login'), {
                'email' : 'test',
                'password' : 'testpassword'
          })
    def test_login_redirect(self):
          response = self.client.post(reverse('login'),{
                'email' : 'test@gmail.com',
                'password' : 'testpassword'
          })
          self.assertRedirects(response, reverse('home'))
    '''

class LoginViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.create(username=self.username, password=self.password)

    def test_get_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_valid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'jenni', 'password': 'jenni'})
        self.assertRedirects(response, self.home_url)

    def test_post_invalid_username(self):
        response = self.client.post(self.login_url, {'username': 'wrong', 'password': self.password})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_invalid_password(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': 'wrong'})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_empty_username(self):
        response = self.client.post(self.login_url, {'username': '', 'password': self.password})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_empty_password(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': ''})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_empty_credentials(self):
        response = self.client.post(self.login_url, {'username': '', 'password': ''})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_nonexistent_user(self):
        response = self.client.post(self.login_url, {'username': 'nonexistent', 'password': 'password'})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_case_insensitive_username(self):
        response = self.client.post(self.login_url, {'username': self.username.upper(), 'password': self.password})
        self.assertRedirects(response, self.home_url)

    def test_post_case_insensitive_password(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password.upper()})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_sql_injection_username(self):
        response = self.client.post(self.login_url, {'username': "' OR 1=1 --", 'password': self.password})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_sql_injection_password(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': "' OR 1=1 --"})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_html_injection_username(self):
        response = self.client.post(self.login_url, {'username': '<script>alert(1)</script>', 'password': self.password})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_html_injection_password(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': '<script>alert(1)</script>'})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_long_username(self):
        long_username = 'a' * 256
        response = self.client.post(self.login_url, {'username': long_username, 'password': self.password})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_long_password(self):
        long_password = 'a' * 256
        response = self.client.post(self.login_url, {'username': self.username, 'password': long_password})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_special_characters_username(self):
        special_username = '!@#$%^&*()'
        response = self.client.post(self.login_url, {'username': special_username, 'password': self.password})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")

    def test_post_special_characters_password(self):
        special_password = '!@#$%^&*()'
        response = self.client.post(self.login_url, {'username': self.username, 'password': special_password})
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Username or Password Do Not Match, Try Again...")