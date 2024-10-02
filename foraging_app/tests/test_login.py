from django.test import TestCase, RequestFactory
#from .Models import User

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
        self.assertEqual(full_name, user.username)

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