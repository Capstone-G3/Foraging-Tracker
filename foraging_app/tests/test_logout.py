import tempfile

from django.test import TestCase
from django.test import Client
import datetime


class Logout(TestCase):

    def setUp(self):
        self.client = Client()
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

        self.user1 = User.create(id=000, name='BobFindings', password='1234', rating='0', badge='Bronze',
                                 profile_image=testImagePath, created_since=datetime.date)
        self.user_profile1 = User_Profile.create(
            first_name='Bob', last_name='S',
            email='Bob@gmail.com', home_address='234 N Ave',
            phone='414-123-4567', gender=1, user_id=000
        )

    def test_isLoggedOut(self):
        self.client.login(username='BobFindings', passowrd='1234')
        self.assertTrue(self.client.session.get('_auth_user_id'))
        response = self.client.get('')
        self.assertEqual(response, 200)

        self.client.logout()
        self.assertFalse('_auth_user_id' in self.client.session)
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_logged_out_from_other_pages(self):
        self.client.login(username='BobFindings', passowrd='1234')
        self.assertTrue(self.client.session.get('_auth_user_id'))
        # simulate client reaching another page(i.e. reaching main feed page) if test does not correctly cover said
        # case
        if self.client.get().path is not '':
            self.client.logout()
            response = self.client.get()
            self.assertEqual(response.path, '/')
            self.assertFalse('_auth_user_id' in self.client.session)
