from django.test import TestCase
from django.test import Client
from folium import (Marker, Map)


class AcceptanceTest(TestCase):
    # set up client, Map and associated Makers to test against in cases
    def setUp(self):
        self.client = Client()
        self.map = Map(location=(0, 0), zoom_start=3)
        self.map.save()
        self.marker = Marker((43.07836095706915, -87.8819686), popup=True).add_to(self.map)
        self.marker.save()

    #   client should be able to view main page upon successful request/response
    def test_home(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    #   client should be able to view map element upon entering main page
    def test_map(self):
        response = self.client.get('')
        self.assertContains(response, self.map)

    #   client should be able to see public markers on page, if they are available
    def test_map_marker(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.marker.icon)

    #   client should be able to see public markers on map in their respective location
    def test_client_sees_correct_markers(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        test_marker = Marker(location=(43.07836095706915, -87.8819686)).add_to(self.map)
        self.assertEqual(self.marker.location, test_marker.location)

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
