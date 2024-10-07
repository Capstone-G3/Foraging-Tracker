from datetime import date

from django.db import IntegrityError
from django.test import TestCase
from unittest.mock import Mock

from foraging_app.models import User, Species, Marker
from foraging_app.models.marker import User_Marker


class TestMarkerModel(TestCase):
    #   test user marker has associated marker id and user id
    #   test user marker saved date is not empty/none
    def test_user_marker(self):
        user1 = User.objects.create(id=5256, username='Bob', password='123', rating=0,
                                    created_since=date.today())
        species1 = Species.objects.create(id=123, name='Species 1', category='fruit'
                                          , scope='testscope', description='Found berry', image='/testImagePath')
        test_marker = Marker.objects.create(id=0000, title='Lion''s mane', latitude=43.07866235729638,
                                            longitude=-87.881974725981,
                                            is_private=False, species=species1, owner=user1)
        user_marker1 = User_Marker.objects.create(user_id=user1, marker_id=test_marker, saved_date=date.today())
        self.assertEqual(user_marker1.user_id, user1)
        self.assertEqual(user_marker1.marker_id, test_marker)
        self.assertIsNotNone(user_marker1.saved_date)

    #   test marker model's OWNER_USER field is the associated  ID of the User creating the marker
    #   test marker model's CREATED_AT, IS_PRIVATE field is not empty/null
    #   test marker model's IS_PRIVATE field is a boolean value
    #   test marker model's ID field is unique

    def test_marker(self):
        test_user1 = User.objects.create(id=1111, username='Bob', password='123', rating=0,
                                         created_since=date.today())
        species1 = Species.objects.create(id=123, name='Species 1', category='fruit'
                                          , scope='testscope', description='Found berry', image='/testImagePath')
        test_marker = Marker.objects.create(id=0000, title='Lion''s mane', latitude=43.07866235729638,
                                            longitude=-87.881974725981,
                                            is_private=False, species=species1, owner_id=test_user1.id)
        self.assertEqual(test_marker.owner_id, test_user1.id)
        self.assertIsNotNone(test_marker.is_private)
        self.assertIsInstance(test_marker.is_private, bool)
        with self.assertRaises(IntegrityError):
            Marker.objects.create(id=0000, title='Test''s mane', latitude=43.07866235729638, longitude=-87.881974725981,
                                  is_private=False, species=species1, owner_id=test_user1.id)