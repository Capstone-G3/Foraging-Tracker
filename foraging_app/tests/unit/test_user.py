from django.test import TestCase
from foraging_app import models
from datetime import date

from foraging_app.models import User, UserProfile


class TestUserModel(TestCase):
    

    def setup(self):
        self.test_user = User.objects.create(username='testUser', email='testUser@uwm.edu', password='helloWorld')

        # self.test_user1 = User.objects.create(ID=1234, user_name='BobsFindings', password=12345, rating=0,
        #                               badge=models.Badge.bronze,
        #                               created_since=date.today())
        # self.test_user2 = User.objects.create(ID=4353, user_name='AliceFindings', password=23445, rating=0,
        #                               badge=models.Badge.Bronze,
        #                               created_since=date.today())
        
        # self.test_user1_profile = User_Profile.objects.create(
        #     first_name='Bob', last_name='Smith',
        #     email='test@gmail.com', home_address='1234 pine',
        #     phone='414-123-456-7890', gender=1, id=12345, user=self.test_user1
        # )


    #   created users fields should not be null/empty
    def test_user(self):
        self.assertIsNotNone(self.test_user)
        
        # self.assertIsNotNone(self.test_user1.id)
        # self.assertIsNotNone(self.test_user1.username)
        # self.assertIsNotNone(self.test_user1.password)
        # self.assertIsNotNone(self.test_user1.rating)
        # self.assertIsNotNone(self.test_user1.badge)
        # self.assertIsNotNone(self.test_user1.created_since)

    # # user model's ID should be a unique field
    # def test_unique_user_ID(self):
    #     with self.assertRaises(AssertionError):
    #         User.create(id=5256, user_name='BobsFindings', password=458657, rating=1,
    #                     badge=models.BADGE.GOLD,
    #                     created_since=date.today())

    # # user model's Username should be a unique field
    # def test_unique_user_name(self):
    #     with self.assertRaises(AssertionError):
    #         User.create(id=1234, user_name='AliceForages', password=23457, rating=1,
    #                     badge=models.Badge.gold,
    #                     created_since=date.today())

    # #   test user profile model has an existing User it's connected to
    # #   test user profile model shares unique ID with its connected USER
    # #   test user model fields that should be strings are indeed instances of STRINGS
    # #   test user's model field GENDER is a valid instance of the gender enum
    # def test_user_profile(self):
    #     self.assertEqual(self.test_user1_profile.user, self.test_user1)
    #     self.assertEqual(self.test_user1_profile.id, self.test_user1.ID)
    #     self.assertIsInstance(self.test_user1.first_name, str)
    #     self.assertIsInstance(self.test_user1_profile.last_name, str)
    #     self.assertIsInstance(self.test_user1_profile.email, str)
    #     self.assertIsInstance(self.test_user1_profile.phone, str)
    #     self.assertIn(self.test_user1_profile.gender, models.Gender)

    # # test badges are valid options {DIA,PLAT,GOLD,SILVER,BRONZE}
    # # test corresponding badge values are in valid range
    # #   test default badge set to Bronze

    # def test_bade_enum(self):
    #     expected_badges = models.Badge.diamond, models.Badge.platimnum, models.Badge.GOLD, models.Badge.silver, models.Badge.bronze
    #     self.assertEqual(expected_badges, models.BADGE)

    #     self.assertGreaterEqual(models.Badge.diamond.value, 100, 000)

    #     self.assertGreaterEqual(models.Badge.platimnum.value, 10, 000)
    #     self.assertLessEqual(models.Badge.platimnum.value, 99, 999)

    #     self.assertGreaterEqual(models.Badge.gold.value, 1, 000)
    #     self.assertLessEqual(models.Badge.gold.value, 9, 999)

    #     self.assertGreaterEqual(models.Badge.silver.value, 100)
    #     self.assertLessEqual(models.Badge.silver.value, 999)

    #     self.assertGreaterEqual(models.Badge.bronze.value, 99)
    #     self.assertLessEqual(models.Badge.bronze.value, 0)

    # # gender should be one fo the following corresponding values(MALE,FEMALE, OTHER) with its associated numerical
    # # values(1, 2, 9)
    # def test_gender_enum(self):
    #     expected_genders = {1, 2, 9}
    #     self.assertContains(expected_genders, models.Gender)
    #     self.assertEqual(models.Gender.male.value, 1)
    #     self.assertEqual(models.Gender.female.value, 2)
    #     self.assertEqual(models.Gender.other.value, 9)

    # # status should be one fo the following corresponding values(ACCEPT, PENDING, REJECT) with its associated numerical
    # # values(0, 1, 2)
    # def test_status_enum(self):
    #     expected_status = {0, 1, 2}
    #     self.assertContains(expected_status, models.Status)
    #     self.assertEqual(models.Status.accept.value, 0)
    #     self.assertEqual(models.Status.pending.value, 1)
    #     self.assertEqual(models.Status.reject.value, 2)