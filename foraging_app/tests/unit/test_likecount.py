from django.test import TestCase

class LikeTest(TestCase):
    def setUp(self):
        pass
    #   TODO UN-COMMENT WHEN LIKE_COUNT IS IMPLEMENTED
    #   test like counter is associated to its corresponding marker and marker owner ID
    # def test_like_count(self):
    #     test_user1 = User.objects.create(id=1111, username='Bob', password='123', rating=0,
    #                                      created_since=date.today())
    #     test_marker = Marker.objects(id=0000, tle='Lion''s mane', latitude=43.07866235729638,
    #                                  longitude=-87.881974725981,
    #                                  created_at=date.today(), is_private=False, species='',
    #                                  owner_user=test_user1)
    #     # test_like_marker = models.like_count(marker_id=test_marker.ID, user_id=test_marker.owner_user)
    #     self.assertEqual(test_like_marker.marker_id, test_marker)
    #     self.assertEqual(test_like_marker.user_id, test_marker.owner_user)
