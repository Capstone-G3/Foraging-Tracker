from django.db import IntegrityError
from django.test import TestCase
from datetime import date
import tempfile
import os

from foraging_app.models.species import Species
from foraging_app.models.user import User
from foraging_app.models.user_profile import User_Profile
from foraging_app.models.marker import Marker
from foraging_app.models.user_marker import User_Marker
# from foraging_app.models.friend import Friend
# from foraging_app.models.friend_request import Friend_Request
# from foraging_app.models.like_count import Like_Count
from foraging_app.models.group import Group
from foraging_app.models.user_group import User_Group


class TestModels(TestCase):
    def setup(self):
        pass

    #   created users fields should not be null/empty
    def test_user(self):
        test_user1 = User.objects.create(username='BobsFindings', password=12345, rating=0,
                                         created_since=date.today())
        self.assertIsNotNone(test_user1.id)
        self.assertIsNotNone(test_user1.username)
        self.assertIsNotNone(test_user1.password)
        self.assertIsNotNone(test_user1.rating)
        self.assertIsNotNone(test_user1.badge)
        self.assertIsNotNone(test_user1.created_since)
        self.assertEqual(test_user1.created_since, date.today())

    # user model's ID should be a unique field
    def test_unique_user_ID(self):
        User.objects.create(id=5256, username='Alice', password='<PASSWORD>', rating=0, created_since=date.today())
        with self.assertRaises(IntegrityError):
            User.objects.create(id=5256, username='BobsFindings', password=458657, rating=1,
                                created_since=date.today())

    #   test user profile model has an existing User it's connected to
    #   test user profile model shares unique ID with its connected USER
    #   test user model fields that should be strings are indeed instances of STRINGS
    #   test user's model field GENDER is a valid instance of the gender enum
    def test_user_profile(self):
        user1 = User.objects.create(id=5256, username='BobsFindings', password='123', rating=0,
                                    created_since=date.today())
        user1_profile = User_Profile(
            first_name='Bob', last_name='Smith',
            email='test@gmail.com', home_address='1234 pine',
            phone='414-123-456-7890', user_id=user1
        )
        user1_profile.gender = 'Male'
        user1_profile.save()
        self.assertEqual(user1_profile.user_id, user1)
        self.assertIsInstance(user1_profile.first_name, str)
        self.assertIsInstance(user1_profile.last_name, str)
        self.assertIsInstance(user1_profile.email, str)
        self.assertIsInstance(user1_profile.phone, str)
        self.assertEqual(user1_profile.gender, 'Male')

    # test badges are valid options {DIA,PLAT,GOLD,SILVER,BRONZE}
    # test corresponding badge values are in valid range
    #   test default badge set to Bronze

    def test_bade_enum(self):
        expected_badges = [("Diamond", 100000), ("Platinum", 10000), ("Gold", 1000), ("Silver", 100), ("Bronze", 0)]
        self.assertEqual(expected_badges, User.badge)

        bronze_badge = User.badge.pop()
        self.assertGreaterEqual(bronze_badge, ("Bronze", 0))
        self.assertLessEqual(bronze_badge, ("Bronze", 99))

        silver_badge = User.badge.pop()
        self.assertGreaterEqual(silver_badge, ('Silver', 100))
        self.assertLessEqual(silver_badge, ('Silver', 999))

        gold_badge = User.badge.pop()
        self.assertGreaterEqual(gold_badge, ('Gold', 1000))
        self.assertLessEqual(gold_badge, ('Gold', 9999))

        platinum_badge = User.badge.pop()
        self.assertGreaterEqual(platinum_badge, ('Platinum', 10000))
        self.assertLessEqual(platinum_badge, ('Platinum', 99999))

        diamond_badge = User.badge.pop()
        self.assertGreaterEqual(diamond_badge, ('Diamond', 100000))

    # gender should be one fo the following corresponding values(MALE,FEMALE, OTHER) with its associated numerical
    # values(1, 2, 9)
    def test_gender_enum(self):
        expected_genders = [("Male", 2), ("Female", 1), ("Other", 9)]
        self.assertEqual(expected_genders, User_Profile.gender)

    # status should be one fo the following corresponding values(ACCEPT, PENDING, REJECT) with its associated numerical
    # values(0, 1, 2)
    # def test_status_enum(self):
    #     expected_status = [('Accept', 0), ('Pending', 1), ('reject', 2)]
    #     self.assertEqual(expected_status, Friend_Request.status)

    #   test user group model's User ID corresponds to an existing members User's ID
    #   test user group model's Group ID corresponds to an existing GROUP ID
    def test_user_group(self):
        user1 = User.objects.create(id=5256, username='Bob', password='123', rating=0,
                                    created_since=date.today())
        test_group = Group.objects.create(id=8342, category='Mushrooms', name='BobGroup', description='',
                                          user_admin=user1)
        user1_group = User_Group.objects.create(user_id=user1, group_id=test_group)
        self.assertEqual(user1_group.user_id, user1)
        self.assertEqual(user1_group.group_id, test_group)

    #   test that Group ID is unique
    #   test that USER_ADMIN field is a valid ID associated to the Group admins ID
    def test_group(self):
        user1 = User.objects.create(id=5256, username='Bob', password='123', rating=0,
                                    created_since=date.today())
        test_group = Group.objects.create(id=8342, category='Mushrooms', name='BobGroup', description='',
                                          user_admin=user1)
        self.assertEqual(test_group.user_admin, user1)
        with self.assertRaises(IntegrityError):
            Group.objects.create(id=1234, category='Fishing', name='BobGroup', description='', user_admin=user1)

    #   test user marker has associated marker id and user id
    #   test user marker saved date is not empty/none
    def test_user_marker(self):
        user1 = User.objects.create(id=5256, username='Bob', password='123', rating=0,
                                    created_since=date.today())
        test_marker = Marker.objects.create(id=0000, title='Lion''s mane', latitude=43.07866235729638,
                                            longitude=-87.881974725981,
                                            created_at=date.today(), is_private=False, species='',
                                            owner_admin=user1)
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
        test_marker = Marker.objects.create(id=0000, title='Lion''s mane', latitude=43.07866235729638,
                                            longitude=-87.881974725981,
                                            created_at=date.today(), is_private=False, species='',
                                            owner_admin=test_user1)
        self.assertEqual(test_marker.owner_user, test_user1)
        self.assertIsNotNone(test_marker.marker.created_at)
        self.assertIsNotNone(test_marker.marker.is_private)
        self.assertIsInstance(test_marker.marker.is_private, bool)
        with self.assertRaises(AssertionError):
            Marker.objects.create(id=0000, title='Lion''s mane', latitude=43.07866235729638, longitude=-87.881974725981,
                                  created_at=date.today(), is_private=False, species='', owner_user=test_user1)

    #   **********UN-COMMENT  WHEN LIKE COUNT IS IMPLEMENTED**********
    #   test like counter is associated to its corresponding marker and marker owner (ID)

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

    #   **********UN-COMMENT  WHEN FRIEND REQUEST IS IMPLEMENTED**********
    #   test friend request has a valid sending user as well as receiving user
    #   test status of request is not empty/null
    #   test request date of request is not empty/null
    # def test_friend_request(self):
    #     test_user1 = User.objects.create(id=2345, username='Bob', password='123', rating=0,
    #                                      created_since=date.today())
    #     test_user2 = User.objects.create(id=5265, username='Alice', password='000', rating=0,
    #                                      created_since=date.today())
    #     friend_request1 = Friend_Request.objects.create(uid_sender=test_user1, uid_reciever=test_user2,
    #                                                     status='Accept', request_date=date.today())
    #     self.assertEqual(friend_request1.uid_sender, test_user1)
    #     self.assertEqual(friend_request1.uid_reciever, test_user2)
    #     self.assertIsNotNone(friend_request1.status)
    #     self.assertIsNotNone(friend_request1.request_date)

    #   **********UN-COMMENT  WHEN FRIEND IS IMPLEMENTED**********
    #   test friend model field user_a and user_b correspond to user and the user that was added as a friend
    # def test_friend(self):
    #     test_user1 = User.objects.create(id=1111, username='Bob', password='123', rating=0,
    #                                      created_since=date.today())
    #     test_user2 = User.objects.create(id=2314, username='Alice', password='000', rating=0,
    #                                      created_since=date.today())
    #     friend1 = Friend.objects.create(user_a=test_user1, user_b=test_user2, saved_date=date.today())
    #
    #     self.assertEqual(friend1.user_a, test_user1)
    #     self.assertEqual(friend1.user_b, test_user2)
    #     self.assertIsNotNone(friend1.saved_date)

    #   test species model fields are not null/empty
    #   test species model field type is an image
    #   test species model fields that require a STRING type are instances of str.

    def test_species(self):
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
        species1 = Species.objects.create(id=123, name='Species 1', category='fruit'
                                          , scope='testscope', description='Found berry', image=testImagePath)
        self.assertIsNotNone(species1.id)
        self.assertIsNotNone(species1.name)
        self.assertIsNotNone(species1.image)
        self.assertIsInstance(species1.category, str)
        self.assertIsInstance(species1.scope, str)
        os.remove(testImagePath)
