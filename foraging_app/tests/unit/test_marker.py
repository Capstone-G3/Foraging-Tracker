from django.test import TestCase
from unittest.mock import Mock

class TestMarkerModel(TestCase):
    #   test user marker has associated marker id and user id
    #   test user marker saved date is not empty/none
    # def test_user_marker(self):
    #     test_marker = models.Marker(id=0000, title='Lion''s mane', latitude=43.07866235729638,
    #                                 longitude=-87.881974725981,
    #                                 created_at=date.today(), is_private=False, species='',
    #                                 owner_admin=self.test_user1.id)
    #     user_marker1 = models.User_Marker(user_id=self.test_user1.id, marker_id=test_marker.id, saved_date=date.today())
    #     self.assertEqual(user_marker1.user_id, test_marker.id)
    #     self.assertEqual(user_marker1.marker_id, test_marker.id)
    #     self.assertIsNotNone(user_marker.saved_date)


     #  **** REMINDER TO BE COMPLETED LATER**** (species portion of model)
    #   test marker model's OWNER_USER field is the associated  ID of the User creating the marker
    #   test marker model's CREATED_AT, IS_PRIVATE field is not empty/null
    #   test marker model's IS_PRIVATE field is a boolean value
    #   test marker model's ID field is unique

    # def test_marker(self):
    #     test_marker = models.Marker(id=0000, title='Lion''s mane', latitude=43.07866235729638,
    #                                 longitude=-87.881974725981,
    #                                 created_at=date.today(), is_private=False, species='',
    #                                 owner_admin=self.test_user1.id)
    #     self.assertEqual(test_marker.owner_user, self.test_user1.id)
    #     self.assertIsNotNone(test_marker.marker.created_at)
    #     self.assertIsNotNone(test_marker.marker.is_private)
    #     self.assertIsInstance(test_marker.marker.is_private, bool)
    #     with self.assertRaises(AssertionError):
    #         Marker.create(id=0000, title='Lion''s mane', latitude=43.07866235729638, longitude=-87.881974725981,
    #                       created_at=date.today(), is_private=False, species='', owner_user=self.test_user1.id)
    
    #   test like counter is associated to its corresponding marker and marker owner (ID)
    # def test_like_count(self):
    #     test_marker = models.MARKER(id=0000, tle='Lion''s mane', latitude=43.07866235729638,
    #                                 longitude=-87.881974725981,
    #                                 created_at=date.today(), is_private=False, species='',
    #                                 owner_user=self.test_user1.id)
    #     test_like_marker = models.like_count(marker_id=test_marker.ID, user_id=test_marker.owner_user)
    #     self.assertEqual(test_like_marker.marker_id, test_marker.id)
    #     self.assertEqual(test_like_marker.user_id, test_marker.owner_user)
    
    pass