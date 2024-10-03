from django.test import TestCase
from foraging_app.forms import UserRegistrationForm, UserProfileForm
from foraging_app.models.user import User

class UserRegistrationFormTest(TestCase):

    def test_valid_form(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'password': 'Testpass123!',
            'confirm_password': 'Testpass123!'
        })
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'password': 'Testpass123!',
            'confirm_password': 'Differentpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords do not match', form.errors['__all__'])

    def test_password_strength(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'password': 'weak',
            'confirm_password': 'weak'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value has at least 8 characters (it has 4).', form.errors['password'])

    def test_missing_username(self):
        form = UserRegistrationForm(data={
            'password': 'Testpass123!',
            'confirm_password': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_missing_password(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'confirm_password': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_missing_confirm_password(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'password': 'Testpass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)

    def test_empty_form(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)
        self.assertIn('confirm_password', form.errors)

class UserProfileFormTest(TestCase):

    def test_valid_form(self):
        form = UserProfileForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'home_address': '123 Main St',
            'phone': '1234567890',
            'gender': 2
        })
        self.assertTrue(form.is_valid())

    def test_invalid_phone(self):
        form = UserProfileForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'home_address': '123 Main St',
            'phone': '12345',
            'gender': 2
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid 10-digit phone number.', form.errors['phone'])

    def test_missing_first_name(self):
        form = UserProfileForm(data={
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'home_address': '123 Main St',
            'phone': '1234567890',
            'gender': 2
        })
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_missing_last_name(self):
        form = UserProfileForm(data={
            'first_name': 'John',
            'email': 'john.doe@example.com',
            'home_address': '123 Main St',
            'phone': '1234567890',
            'gender': 'M'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_missing_email(self):
        form = UserProfileForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'home_address': '123 Main St',
            'phone': '1234567890',
            'gender': 'M'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_missing_home_address(self):
        form = UserProfileForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'gender': 'M'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('home_address', form.errors)

    def test_missing_phone(self):
        form = UserProfileForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'home_address': '123 Main St',
            'gender': 'M'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_missing_gender(self):
        form = UserProfileForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'home_address': '123 Main St',
            'phone': '1234567890'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('gender', form.errors)

    def test_empty_form(self):
        form = UserProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('home_address', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('gender', form.errors)
