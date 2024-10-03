from django.test import TestCase
from django.test import Client
from folium.map import Figure

class TestHomeAcceptance(TestCase):
    # set up client, Map and associated Makers to test against in cases
    def setUp(self):
        self.client = Client()
        
    def test_home(self):
        """
            Client should be able to view main page upon successful request/response
        """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_map(self):
        """
            Client should be able to view map element upon entering main page
        """
        response = self.client.get('')
        self.assertTrue(isinstance(response.context['map'], Figure))

  