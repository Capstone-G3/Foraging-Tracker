from django.test import TestCase
from foraging_app import models
from datetime import date
import tempfile
import imghdr
import os

from foraging_app.models import User


class TestModels(TestCase):
    def setup(self):
        self.test_user1 = User.create(ID=1234, user_name='BobsFindings', password=12345, rating=0,
                                      badge=models.Badge.bronze,
                                      created_since=date.today())
        self.test_user2 = User.create(ID=4353, user_name='AliceFindings', password=23445, rating=0,
                                      badge=models.Badge.Bronze,
                                      created_since=date.today())
        self.test_user1_profile = User_Profile.create(
            first_name='Bob', last_name='Smith',
            email='test@gmail.com', home_address='1234 pine',
            phone='414-123-456-7890', gender=1, id=12345, user=self.test_user1
        )
        self.test_group2 = Group.create(id=1234, category='Mushroom', name='Group3', description='',
                                        user_admin=self.test_user1.ID)
        self.test_group = models.Group(id=8342, category='Mushrooms', name='Bob''s'' Group', description='',
                                       user_admin=self.test_user1.ID)
        self.test_user1_group = models.User_Group(user_id=self.test_user1.ID, group_id=self.test_group.ID,
                                                  joined_date=date.today())
        self.test_species = models.Species(id=7357, name='strawbery', category='Plant', description='', scope='berry',
                                           image='')

    #   created users fields should not be null/empty
    def test_user(self):
        self.assertIsNotNone(self.test_user1.id)
        self.assertIsNotNone(self.test_user1.username)
        self.assertIsNotNone(self.test_user1.password)
        self.assertIsNotNone(self.test_user1.rating)
        self.assertIsNotNone(self.test_user1.badge)
        self.assertIsNotNone(self.test_user1.created_since)

    # user model's ID should be a unique field
    def test_unique_user_ID(self):
        with self.assertRaises(AssertionError):
            User.create(id=5256, user_name='BobsFindings', password=458657, rating=1,
                        badge=models.BADGE.GOLD,
                        created_since=date.today())

    # user model's Username should be a unique field
    def test_unique_user_name(self):
        with self.assertRaises(AssertionError):
            User.create(id=1234, user_name='AliceForages', password=23457, rating=1,
                        badge=models.Badge.gold,
                        created_since=date.today())

    #   test user profile model has an existing User it's connected to
    #   test user profile model shares unique ID with its connected USER
    #   test user model fields that should be strings are indeed instances of STRINGS
    #   test user's model field GENDER is a valid instance of the gender enum
    def test_user_profile(self):
        self.assertEqual(self.test_user1_profile.user, self.test_user1)
        self.assertEqual(self.test_user1_profile.id, self.test_user1.ID)
        self.assertIsInstance(self.test_user1.first_name, str)
        self.assertIsInstance(self.test_user1_profile.last_name, str)
        self.assertIsInstance(self.test_user1_profile.email, str)
        self.assertIsInstance(self.test_user1_profile.phone, str)
        self.assertIn(self.test_user1_profile.gender, models.Gender)

    # test badges are valid options {DIA,PLAT,GOLD,SILVER,BRONZE}
    # test corresponding badge values are in valid range
    #   test default badge set to Bronze

    def test_bade_enum(self):
        expected_badges = models.Badge.diamond, models.Badge.platimnum, models.Badge.GOLD, models.Badge.silver, models.Badge.bronze
        self.assertEqual(expected_badges, models.BADGE)

        self.assertGreaterEqual(models.Badge.diamond.value, 100, 000)

        self.assertGreaterEqual(models.Badge.platimnum.value, 10, 000)
        self.assertLessEqual(models.Badge.platimnum.value, 99, 999)

        self.assertGreaterEqual(models.Badge.gold.value, 1, 000)
        self.assertLessEqual(models.Badge.gold.value, 9, 999)

        self.assertGreaterEqual(models.Badge.silver.value, 100)
        self.assertLessEqual(models.Badge.silver.value, 999)

        self.assertGreaterEqual(models.Badge.bronze.value, 99)
        self.assertLessEqual(models.Badge.bronze.value, 0)

    # gender should be one fo the following corresponding values(MALE,FEMALE, OTHER) with its associated numerical
    # values(1, 2, 9)
    def test_gender_enum(self):
        expected_genders = {1, 2, 9}
        self.assertContains(expected_genders, models.Gender)
        self.assertEqual(models.Gender.male.value, 1)
        self.assertEqual(models.Gender.female.value, 2)
        self.assertEqual(models.Gender.other.value, 9)

    # status should be one fo the following corresponding values(ACCEPT, PENDING, REJECT) with its associated numerical
    # values(0, 1, 2)
    def test_status_enum(self):
        expected_status = {0, 1, 2}
        self.assertContains(expected_status, models.Status)
        self.assertEqual(models.Status.accept.value, 0)
        self.assertEqual(models.Status.pending.value, 1)
        self.assertEqual(models.Status.reject.value, 2)

    #   test user group model's User ID corresponds to an existing members User's ID
    #   test user group model's Group ID corresponds to an existing GROUP ID
    #   test validation of creation date is entered
    def test_user_group(self):
        self.assertEqual(self.test_user1_group.USER_ID, self.test_user1.id)
        self.assertEqual(self.test_user1_group.ID, self.test_group.id)
        self.assertIsNotNone(models.User_Group.joined_date)

    #   test that Group ID is unique
    #   test that USER_ADMIN field is a valid ID associated to the Group admins ID
    def test_group(self):
        self.assertEqual(self.test_group.user_admin, self.test_user1.ID)
        with self.assertRaises(AssertionError):
            Group.create(id=1234, category='Fishing', name='Group5', description='', user_admin=self.test_user1.id)

    #   test user marker has associated marker id and user id
    #   test user marker saved date is not empty/none
    def test_user_marker(self):
        test_marker = models.Marker(id=0000, title='Lion''s mane', latitude=43.07866235729638,
                                    longitude=-87.881974725981,
                                    created_at=date.today(), is_private=False, species='',
                                    owner_admin=self.test_user1.id)
        user_marker1 = models.User_Marker(user_id=self.test_user1.id, marker_id=test_marker.id, saved_date=date.today())
        self.assertEqual(user_marker1.user_id, test_marker.id)
        self.assertEqual(user_marker1.marker_id, test_marker.id)
        self.assertIsNotNone(user_marker.saved_date)

    #  **** REMINDER TO BE COMPLETED LATER**** (species portion of model)
    #   test marker model's OWNER_USER field is the associated  ID of the User creating the marker
    #   test marker model's CREATED_AT, IS_PRIVATE field is not empty/null
    #   test marker model's IS_PRIVATE field is a boolean value
    #   test marker model's ID field is unique

    def test_marker(self):
        test_marker = models.Marker(id=0000, title='Lion''s mane', latitude=43.07866235729638,
                                    longitude=-87.881974725981,
                                    created_at=date.today(), is_private=False, species='',
                                    owner_admin=self.test_user1.id)
        self.assertEqual(test_marker.owner_user, self.test_user1.id)
        self.assertIsNotNone(test_marker.marker.created_at)
        self.assertIsNotNone(test_marker.marker.is_private)
        self.assertIsInstance(test_marker.marker.is_private, bool)
        with self.assertRaises(AssertionError):
            Marker.create(id=0000, title='Lion''s mane', latitude=43.07866235729638, longitude=-87.881974725981,
                          created_at=date.today(), is_private=False, species='', owner_user=self.test_user1.id)

    #   test like counter is associated to its corresponding marker and marker owner (ID)
    def test_like_count(self):
        test_marker = models.MARKER(id=0000, tle='Lion''s mane', latitude=43.07866235729638,
                                    longitude=-87.881974725981,
                                    created_at=date.today(), is_private=False, species='',
                                    owner_user=self.test_user1.id)
        test_like_marker = models.like_count(marker_id=test_marker.ID, user_id=test_marker.owner_user)
        self.assertEqual(test_like_marker.marker_id, test_marker.id)
        self.assertEqual(test_like_marker.user_id, test_marker.owner_user)

    #   test friend request has a valid sending user as well as receiving user
    #   test status of request is not empty/null
    #   test request date of request is not empty/null
    def test_friend_request(self):
        # friend1 = models.FRIEND(USER_A=self.Test_User1, USER_B=self.Test_User2, SAVED_DATE=date.today())
        friend_request1 = models.Friend_Request(uid_sender=self.test_user1, uid_reciever=self.test_user2,
                                                STATUS=models.Status.pending, REQUEST_DATE=date.today())
        self.assertEqual(friend_request1.uid_sender, self.test_user1)
        self.assertEqual(friend_request1.uid_reciever, self.test_user2)
        self.assertIsNotNone(friend_request1.status)
        self.assertIsNotNone(friend_request1.request_date)

    #   test friend model field user_a and user_b correspond to user and the user that was added as a friend
    def test_friend(self):
        friend1 = models.Friend(user_a=self.test_user1, user_b=self.test_user2, saved_date=date.today())
        self.assertEqual(friend1.user_a, self.test_user1)
        self.assertEqual(friend1.user_b, self.test_user2)
        self.assertIsNotNone(friend1.saved_date)

    #   test species model fields are not null/empty
    #   test species model field type is an image
    #   test species model fields that require a STRING type are instances of str.
    def test_species(self):
        self.assertIsNotNone(models.Species.id)
        self.assertIsInstance(models.Species.id, str)
        self.assertIsNotNone(models.Species.image)
        self.assertIsInstance(models.Species.category, str)
        self.assertIsInstance(models.Species.scope, str)
        testImagePath = tempfile.NamedTemporaryFile(suffix=".jpg").name
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
        models.Species.Image = testImagePath
        imageType = imghdr.what(models.Species.Image)
        self.assertIsNotNone(imageType)
        os.remove(testImagePath)
