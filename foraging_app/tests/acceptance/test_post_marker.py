from django.test import TestCase
from django.test import Client

# TODO : The responsibity for Posting a Marker does not exist yet.
class TestHomeMarker(TestCase):
    def setUp(self):
        self.client = Client()
    
    #   client should be able to see public markers on page, if they are available
    def test_map_marker(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.map)

    def test_client_sees_correct_markers(self):
        """
            Client should be able to see public markers on map in their respective location
            A client first must post a Marker to the server, then 
        """
        response = self.client.get('')

    # client should be able to access login page from home page if they are not logged in
    def test_non_account_to_login(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

        if not self.client.is_authenticated:
            self.assertContains(response, 'name="login"')
            response = self.client.get('/login/')
            self.assertEqual(response.status_code, 200)

    #   non logged in client should be able to click on public markers and be redirected to user's public profile
    def test_non_loggedIn_interact_marker(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        if not self.client.is_authenticated:
            self.assertEqual(self.marker.options.get(), True)
