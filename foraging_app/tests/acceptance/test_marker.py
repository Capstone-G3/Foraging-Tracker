from django.test import TestCase
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

from foraging_app.models.user import User, User_Profile
from foraging_app.models.marker import User_Marker
from foraging_app.models.marker import Marker as MarkerModel
from foraging_app.models import Species as SpeciesModel
from foraging_app.forms.marker import MarkerCreateForm, MarkerEditForm

from unittest.mock import Mock

from folium import Figure, Map, Marker
from folium.plugins import MarkerCluster

# TODO : The responsibity for Posting a Marker does not exist yet.
class TestCreateMarker(TestCase):
    def setUp(self):
        # Client
        self.client = Client()

        # Backend User
        user = User.objects.create_user(username="realuser123",
                                password="secret",
                                email="realuser@uwm.edu")
        
        User_Profile.objects.create(home_address="123 BLV",
                                    phone="123-456-7899",
                                    gender=2,
                                    user_id=user)
        
        self.valid_form = {
            'longitude' : 90,
            'latitude' : 45,
            'title' : "Cat",
            'is_private' : False,
            # TODO : Need a real image binaries.
            'image' : SimpleUploadedFile(
                    name='test_image.jpg',
                    content=b'',
                    content_type='image/jpeg'),
            'description' : "This is tested content to be embedded.",
            'species' : '',
            'owner' : user
        }

        self.invalid_form = {
            'longitude' : 90,
            'latitude' : 45,
            'title' : "<p>Cat</p>",
            'is_private' : False,
            'image' : SimpleUploadedFile(name='cat.jpeg', content=b'representation of binary content', content_type='image/jpeg'),
            'description' : """
            <html>
                <body>
                    <p>Html Injection</p>
                </body>
            </html>
            """,
            'species' : ''
        }
    
    def client_log_in(self):
        # Client must be authenticated first. 
        logged = self.client.login(username="realuser123",password="secret")
        # Confirmed the user logged in
        self.assertTrue(logged)

    def test_post_marker_successfully_when_user_logged_in_with_valid_content(self):
        """
            Client that is logged in should be able to post a new marker with contents.
        """

        # Login
        self.client_log_in()

        marker_form = MarkerCreateForm(data=self.valid_form)
        print(marker_form.errors)
        self.assertTrue(marker_form.is_valid())

        # User successfully logged in, they must be able to post a marker
        post_response = self.client.post("/marker/create", data=marker_form,follow=True)
        # Successfully done 
        self.assertEqual(post_response.status_code,200)
        # Checking the main page for the posted marker
        response = self.client.get('')
        # The homepage must contain the map context
        home_map_figure = response.context['map']
        
        # Checking the map context in details
        self.assertTrue(isinstance(home_map_figure, Figure))
        # Expect the first child of Figure is Map itself.
        # Since everything is packed inside Map, the only child of Figure is Map.
        home_map = list(home_map_figure._children.items())[0][1]
        self.assertTrue(isinstance(home_map, Map))
        
        marker_cluster = None
        # Looking for the Cluster within the Map. (Marker Cluster contains all Markers)
        # Search takes O(n) through list.
        for key,value in home_map._children.items():
            if isinstance(value, MarkerCluster):
                marker_cluster = value
                break
        self.assertIsNotNone(marker_cluster)

        # Markers exist within the Marker Cluster
        matching_marker = None
        for key,value in dict(marker_cluster._children.items()).items():
            if isinstance(value,Marker):
                [(popup_key, popup_value)] = value._children._children.items()
                [(html_key, html_value)] = list(popup_value.html._children.items())
                # Verified that the marker content of finding is equivalent to the posted already.
                # Otherwise matching_marker will remained None (failed the test last line.)
                if html_value[0] == marker_content: # TODO fix.
                    matching_marker = value
                # Since found a single posted marker
                break
        self.assertIsNotNone(matching_marker)

    def test_post_marker_fail_when_user_not_log_in(self):
        """
            Client should not be able to post a marker when not sign in.
        """
        # No authentication step.
        valid_content = "None-Existing" # TODO : Valid content?
        response = self.client.post("/marker/create", {"longitude" : 90, "latitude" : 90, "content" : valid_content})
        self.assertEqual(response.status_code, 401) # Unauthorized -> possibly redirect?
        self.assertEqual(response.context['error'], "Please sign in to continue.") # error context with a message


    def test_post_failed_when_html_injection_user_not_logged_in(self):
        """
            Client should not be able to post a marker with unaccepted contents even with logged in authorization.
        """
        # Login
        self.client_log_in()
        # Failed point.
        content="<html><head><body>Some content</body></head></html>" # For sure incorrect content
        response = self.client.post('/marker/create', {'longitude' : 90, 'latitude' : 90, 'content' : content})
        self.assertEqual(response.status_code, 401) #Is not logged in.
        self.assertEqual(response.context['error'], "Please sign in to continue.") 
    
    def test_post_failed_when_html_injection_user_logged_in(self):
        """
            Client should not be able to post a marker with unaccepted contents, though user is not logged in.
        """
        content="<html><head><body>Some content</body></head></html>" # For sure incorrect content
        response = self.client.post('/marker/create',{'longitude' : 90, 'latitude' : 90, 'content' : content})
        self.assertEqual(response.status_code, 406) # Can not generate response for such content.
        self.assertEqual(response.context['error'], "Unacceptable content") # Prevent HTML injection
    
class TestEditMarker(TestCase):
    """
        Must pass the criteria for Edit a Marker
        NOTE: Marker location is locked, trying to update location will fail.
    """
    def setUp(self):
        self.client = Client()

        # Backend User
        user = User.objects.create_user(username="realuser123",
                                password="secret",
                                email="realuser@uwm.edu")
        
        User_Profile.objects.create(home_address="123 BLV",
                                    phone="123-456-7899",
                                    gender=2,
                                    user_id=user)
        
        # Client must be logged in.
        logged_in = self.client.login(username="realuser123", password='secret')
        self.assertTrue(logged_in)

        #TODO : Marker Form
        # Create 10 different markers with the same user.
        for i in range(10):
            data = {
                'Longitude' : i + 90,
                'Latitude' : i + 90,
                'Content' : "Content : " + str(i)
            }
            form = MarkerCreateForm(data=data)
            create_response = self.client.post("/marker/create",{'form' : form})
            # TODO : Must have creation functionality.
            self.assertEquals(create_response, 200)
        
        query_user_marker_list = list(User_Marker.objects.filter(user_id=user.id))
        self.markers = []
        for marker_user in query_user_marker_list:
            self.markers.append(Marker.objects.get(id=marker_user.marker_id))

    def test_edit_marker_successful_when_exist_user_logged_in_owned_content_valid(self):
        """
            Marker is successfully edit when :
            1. Marker Exist
            2. User Logged In
            3. User owned the Marker
            4. Content is valid
        """
        # User logged in.

        # marker/<int:marker_id>/edit
        # The following marker ID is retrieved based on User ID, therefore User owned the marker.
        marker_path = '/marker/'+ self.markers[0].id
        # Marker Exist.
        edit_response = self.client.get(marker_path)
        self.assertEquals(edit_response.status_code, 200)

        # New data is valid.
        data = {
            'content': "New Content"
        }
        # TODO : Edit Form.
        form = MarkerEditForm(data=data)
        change_marker_details_response = self.client.post(marker_path, {'form' : form}, follow=True)
        self.assertRedirects(change_marker_details_response, marker_path)

    
    # Multiple types of invalid contents
    def test_edit_marker_fail_when_exist_user_logged_in_owned_content_html_injection(self):
        """
            Marker failed to edit when :
            1. Content is HTML.
        """
        # User logged in
        marker_path = '/marker/'+ self.markers[0].id
        response = self.client.get(marker_path)
        self.assertEqual(response.status_code, 200)

        data = { 
            'content' : '<html><head></head><body>Injection Content.</body></html>'
        }
        form = MarkerEditForm(data=data)
        edit_marker_response = self.client.post(marker_path, {'form' : form})
        # Unaccept 
        self.assertEqual(edit_marker_response.status_code, 406) # Can not generate a response for such content
        self.assertEqual(edit_marker_response.context['error'], "Unaccepted Content.")

    def test_edit_marker_fail_when_exist_user_logged_in_owned_content_script_injection(self):
        """
            Marker failed to edit when :
            1. Content is JavaScript or other Injection.
        """
         # User logged in
        marker_path = '/marker/'+ self.markers[0].id
        response = self.client.get(marker_path)
        self.assertEqual(response.status_code, 200)

        data = { 
            'content' : 'function queryDocument(){let jquery = document.querySelectorAll("p"); return jquery;}'
        }
        form = MarkerEditForm(data=data)
        edit_marker_response = self.client.post(marker_path, {'form' : form})
        # Unaccept 
        self.assertEqual(edit_marker_response.status_code, 406)
        self.assertEqual(edit_marker_response.context['error'], "Unaccepted Content.")

    def test_edit_marker_fail_when_exist_user_logged_in_owned_content_incorrect_format(self):
        """
            Marker failed to edit when :
            1. Content is incorrectly Format.
        """
         # User logged in
        marker_path = '/marker/'+ self.markers[0].id
        response = self.client.get(marker_path)
        self.assertEqual(response.status_code, 200)

        form = MarkerEditForm() # TODO
        edit_marker_response = self.client.post(marker_path, {'form' : form})
        # Unaccept 
        self.assertEqual(edit_marker_response.status_code, 406)
        self.assertEqual(edit_marker_response.context['error'], "Unaccepted Content.")
    
    def test_edit_marker_fail_when_exist_user_logged_in_not_owned_content_valid(self):
        """
            Marker failed to edit when :
            1. Not owned by User
        """
        #Signed in.

        # Guaranteed the following marker does not own by User.
        not_own_marker_id = self.markers[len(self.markers) - 1].id + 1
        #Guaranteed exist.
        mock_user = Mock(spec=User)
        MarkerModel.objects.create(id=not_own_marker_id, owner=mock_user)

        marker_path = '/marker/'+ not_own_marker_id
        get_response= self.client.get(marker_path)
        self.assertEqual(get_response.status_code, 200)

        data = { 
            'content' : 'Actual Data.'
        }
        form = MarkerEditForm(data=data)
        edit_response = self.client.post(marker_path + '/edit', {'form' : form})
        self.assertEqual(edit_response.status_code, 401) #Unauthorized.

    def test_edit_marker_fail_when_exist_user_not_logged_in(self):
        """
            Marker failed to edit when :
            1. User is not logged in
        """
        logged_out = self.client.logout()
        # User owned the marker but is not logged in.
        marker_path = '/marker/'+ self.markers[0]
        get_response = self.client.get(marker_path + "/edit", follow=True)
        self.assertRedirects(get_response, '/login') # Unauthorized
        
        data = {    
            'content' : 'Actual Data.'
        }
        form = MarkerEditForm(data=data)
        post_response = self.client.post(marker_path + '/edit', {'form' : form}, follow=True)
        self.assertEqual(post_response.status_code, 401) # Unauthorized

    def test_edit_marker_fail_when_not_exist_user_logged_in(self):
        """
            Even the user is logged in, there is no marker to edit.
        """
        # User Logged In.
        with self.assertRaises(MarkerModel.DoesNotExist):
             # In Test Database, this does not exist. (Do not use production database).
            Marker.objects.get(id=100000000)


    def test_edit_marker_fail_when_exist_user_logged_in_owned_invalid_payload(self):
        """
            Marker failed to edit when user upload an invalid payload containing :
            1. Longitude
            2. Latitude
        """
        # User logged in.
        marker_path = '/marker/'+ self.markers[0]
        get_response = self.client.get(marker_path + "/edit")
        self.assertEqual(get_response.status_code, 200)

        data = {
            "longitude" : 90,
            "latitude" : 90,
            "content" : "Valid content." 
        }
        post_response = self.client.post(marker_path + '/edit', {
            'longitude' : data['longitude'],
            'latitude' : data['latitude'],
            'form' : MarkerEditForm(data=data['content'])
            }
        )
        self.assertEqual(post_response.status_code, 406)
        self.assertEqual(post_response.context['error'], "Unaccept Content.")

class TestDeleteMarker(TestCase):
    """
        Marker successfully removed after meeting the criteria:
        1. User must own it
        2. User must logged in
        3. The removing marker must exist
    """
    def setUp(self):
        self.client = Client()

        # Backend User
        user = User.objects.create_user(username="realuser123",
                                password="secret",
                                email="realuser@uwm.edu")
        
        User_Profile.objects.create(home_address="123 BLV",
                                    phone="123-456-7899",
                                    gender=2,
                                    user_id=user)
        
        #TODO : Marker Form
        # Create 10 different markers with the same user.
        for i in range(10):
            data = {
                'Longitude' : i + 90,
                'Latitude' : i + 90,
                'Content' : "Content : " + str(i)
            }
            form = MarkerCreateForm(data=data)
            create_response = self.client.post("/marker/create", {'form' : form})
            # TODO : Must have creation functionality.
            self.assertEquals(create_response, 200)
        
        query_user_marker_list = list(User_Marker.objects.filter(user_id=user.id))
        self.markers = []
        for marker_user in query_user_marker_list:
            self.markers.append(Marker.objects.get(id=marker_user.marker_id))

        logged_in = self.client.login(username='realuser123', password='secret')
        self.assertTrue(logged_in)
                    

    def test_delete_successful_when_exist_user_logged_in_owned(self):
        # User logged in

        # Represent the marker that user owned.
        marker_id = self.markers[0].id 
        marker_path = '/marker/' + marker_id
        

        initial_response = self.client.get(marker_path)
        self.assertEqual(initial_response.status_code, 200) #Exist.
        
        # Post to the server confirmed that user want to delete the user.
        post_response = self.client.post(marker_path + '/delete', follow=True)
        self.assertRedirects(post_response, '/markers')
        self.assertEqual(post_response.status_code, 301) # Redirect

        # Can't get the marker page anymore.
        get_response = self.client.get(marker_path)
        self.assertEqual(get_response.status_code, 404) # Can't find when View.

        # Doesn't exist in our Database.
        query_marker = MarkerModel.objects.get(id=marker_id)
        self.assertIsNone(query_marker)


    def test_delete_fail_when_exist_user_logged_in_not_owned(self):
        #User is current logged in.

        # Guarateed a mock Marker object inside database.
        out_range_id = self.markers[len(self.markers) - 1] + 1
        user = Mock(spec=User)
        marker = MarkerModel.objects.create(id=out_range_id, owner=user)

        marker_path = '/marker/' + marker.id
        get_response = self.client.get(marker_path)
        self.assertEqual(get_response.status_code, 200) # Exist marker page.

        post_response = self.client.post(marker_path + "/delete", follow=True)
        self.assertEqual(post_response.status_code, 401) # Unauthorized

        retry_get_response = self.client.get(marker_path)
        self.assertEqual(retry_get_response.status_code, 200) # Still available.

        # Query
        found_marker = MarkerModel.objects.get(id=marker.id)
        self.assertIsNotNone(found_marker)
        self.assertEqual(found_marker, marker)

    def test_delete_fail_when_exist_user_not_logged_in(self):
        # Currently Logged in

        marker_id = self.markers[0].id
        marker_path = '/marker/' + str(marker_id)
        get_response = self.client.get(marker_path)
        self.assertEqual(get_response.status_code, 200) # Valid

        # User logged out
        self.client.logout()

        # Request for the marker page.
        retry_get_response = self.client.get(marker_path, follow=True)
        #Redirect to login page
        self.assertRedirects(retry_get_response, '/login')
        self.assertEqual(retry_get_response.status_code, 301) # Redirects

        post_response = self.client.post(marker_path + '/delete', follow=True)
        self.assertEqual(post_response.status_code, 401) # Unauthorized


    def test_delete_fail_when_not_exist(self):
        # Currently Logged In 

        # Guaranteed does not exist.
        marker_path = '/marker/' + str(1000000)
        get_response = self.client.get(marker_path,follow=True)
        self.assertEqual(get_response.status_code, 404) # Not Found.

        post_response = self.client.post(marker_path + '/delete', follow=True)
        self.assertEqual(post_response.status_code, 404) # Not Found.


class TestViewMarker(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create(
            username='realuser123',
            password='secret',
            email='realuser123@uwm.edu'
            )
        User_Profile.objects.create(
            user_id = user,
            home_address="123 BLV",
            phone="123-456-7899",
            gender=2
        )

        logged_in = self.client.login(username='realuser123', password='secret')
        self.asserTrue(logged_in)

        #TODO : Marker Form
        # Create 10 different markers with the same user.
        for i in range(10):
            data = {
                'Longitude' : i + 90,
                'Latitude' : i + 90,
                'Content' : "Content : " + str(i)
            }
            form = MarkerCreateForm(data=data)
            create_response = self.client.post("/marker/create", {'form' : form})
            # TODO : Must have creation functionality.
            self.assertEquals(create_response, 200)
        
        query_user_marker_list = list(User_Marker.objects.filter(user_id=user.id))
        self.markers = []
        for marker_user in query_user_marker_list:
            self.markers.append(Marker.objects.get(id=marker_user.marker_id))

        
    def  test_view_successful_when_exist_user_logged_in_self_marker(self):

        pass

    def test_view_successful_when_exist_user_logged_in_other_marker(self):
        pass

    def test_view_fail_when_exist_user_not_logged_in(self):
        pass

    def test_view_fail_when_exist_user_not_logged_in_other_marker(self):
        """
            This case refers to as User deactivated their profile then checking their profile after.
        """
        pass 
    
    def test_view_fail_when_not_exist_user_logged_in_self_marker(self):
        pass

    def test_view_fail_when_not_exist_user_logged_in_other_marker(self):
        pass