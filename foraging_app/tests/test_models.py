from django.test import TestCase
from foraging_app import models
from datetime import date


class TestModels(TestCase):
    def setup(self):
        self.Test_User1 = User.create(ID=1234, USER_NAME='BobsFindings', PASSWORD=12345, RATING=0,
                                      BADGE=models.BADGE.BRONZE,
                                      CREATED_SINCE=date.today())
        self.Test_User1_Profile = User_Profile.create(
            first_name='Bob', last_name='Smith',
            email='test@gmail.com', home_address='1234 pine',
            phone='414-123-456-7890', gender=1, ID=12345, USER=self.Test_User1
        )

    #   created users fields should not be none/empty
    def test_user(self):
        self.assertIsNotNone(self.Test_user1.ID)
        self.assertIsNotNone(self.Test_user1.USERNAME)
        self.assertIsNotNone(self.Test_user1.PASSWORD)
        self.assertIsNotNone(self.Test_user1.RATING)
        self.assertIsNotNone(self.Test_user1.BADGE)
        self.assertIsNotNone(self.Test_user1.CREATED_SINCE)

    # user model's ID should be a unique field
    def test_unique_user_ID(self):
        with self.assertRaises(AssertionError):
            User.create(ID=5256, USER_NAME='BobsFindings', PASSWORD=458657, RATING=1,
                        BADGE=models.BADGE.GOLD,
                        CREATED_SINCE=date.today())

    # user model's Username should be a unique field
    def test_unique_user_name(self):
        with self.assertRaises(AssertionError):
            User.create(ID=1234, USER_NAME='AliceForages', PASSWORD=23457, RATING=1,
                        BADGE=models.BADGE.GOLD,
                        CREATED_SINCE=date.today())

    #   test user profile model has an existing User its connected to
    #   test user profile model shares unique ID with its connected USER
    #   test user model fields that should be strings are indeed instances of STRINGS
    #   test user's model field GENDER is a valid instance of the gender enum
    def test_user_profile(self):
        self.assertEqual(self.Test_User1_Profile.USER, self.Test_User1)
        self.assertEqual(self.Test_User1_Profile.ID, self.Test_User1.ID)
        self.assertIsInstance(self.Test_User1.FIRST_NAME, str)
        self.assertIsInstance(self.Test_User1_Profile.LAST_NAME, str)
        self.assertIsInstance(self.Test_User1_Profile.EMAIL, str)
        self.assertIsInstance(self.Test_User1_Profile.PHONE, str)
        self.assertIn(self.Test_User1_Profile.GENDER, models.GENDER)

    # test badges are valid options {DIA,PLAT,GOLD,SILVER,BRONZE}
    # test corresponding badge values are in valid range
    #   test default badge set to Bronze

    def test_bade_enum(self):
        expected_badges = models.Badge.DIAMOND, models.BADGE.PLATINUM, models.BADGE.GOLD, models.BADGE.SILVER, models.BADGE.BRONZE
        self.assertEqual(expected_badges, models.BADGE)

        self.assertGreaterEqual(models.BADGE.DIAMOND.value, 100, 000)

        self.assertGreaterEqual(models.BADGE.PLATINUM.value, 10, 000)
        self.assertLessEqual(models.BADGE.PLATINUM.value, 99, 999)

        self.assertGreaterEqual(models.BADGE.GOLD.value, 1, 000)
        self.assertLessEqual(models.BADGE.GOLD.value, 9, 999)

        self.assertGreaterEqual(models.BADGE.SILVER.value, 100)
        self.assertLessEqual(models.BADGE.SILVER.value, 999)

        self.assertGreaterEqual(models.BADGE.BRONZE.value, 99)
        self.assertLessEqual(models.BADGE.BRONZE.value, 0)

    # gender should be one fo the following corresponding values(MALE,FEMALE, OTHER) with its associated numerical
    # values(1, 2, 9)
    def test_gender_enum(self):
        expected_genders = {1, 2, 9}
        self.assertContains(expected_genders, models.GENDER)
        self.assertEqual(models.GENDER.MALE.value, 1)
        self.assertEqual(models.GENDER.FEMALE.value, 2)
        self.assertEqual(models.GENDER.OTHER.value, 9)

    # status should be one fo the following corresponding values(ACCEPT, PENDING, REJECT) with its associated numerical
    # values(0, 1, 2)
    def test_status_enum(self):
        expected_status = {0, 1, 2}
        self.assertContains(expected_status, models.STATUS)
        self.assertEqual(models.STATUS.ACCEPT.value, 0)
        self.assertEqual(models.STATUS.PENDING.value, 1)
        self.assertEqual(models.STATUS.REJECT.value, 2)

    def test_user_group(self):
        pass

    def test_like_count(self):
        pass

    def test_friend_request(self):
        pass

    def test_friend(self):
        pass

    def test_marker(self):
        pass

    def test_species(self):
        pass

    def test_user_marker(self):
        pass
