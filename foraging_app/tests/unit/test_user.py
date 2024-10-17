from django.db import IntegrityError
from django.test import TestCase
from foraging_app import models
from datetime import date

from foraging_app.models import User
from foraging_app.models.user import User_Profile


class TestUserModel(TestCase):

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
        self.assertIsNotNone(test_user1.BADGE)
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
            home_address='1234 pine',
            phone='414-123-456-7890', user_id=user1, gender=2
        )
        user1_profile.save()
        self.assertEqual(user1_profile.user_id, user1)
        self.assertIsInstance(user1_profile.phone, str)
        self.assertEqual(user1_profile.gender, 2)

    # test badges are valid options {DIA,PLAT,GOLD,SILVER,BRONZE}
    # test corresponding badge values are in valid range
    #   test default badge set to Bronze

    def test_bade_enum(self):
        expected_badges = (("Diamond", 100000), ("Platinum", 10000), ("Gold", 1000), ("Silver", 100), ("Bronze", 10))
        self.assertEqual(expected_badges, User.BADGE)
        #
        bronze_badge = User.BADGE[4]
        self.assertGreaterEqual(bronze_badge, ("Bronze", 0))
        self.assertLessEqual(bronze_badge, ("Bronze", 99))
        #
        silver_badge = User.BADGE[3]
        self.assertGreaterEqual(silver_badge, ('Silver', 100))
        self.assertLessEqual(silver_badge, ('Silver', 999))

        gold_badge = User.BADGE[2]
        self.assertGreaterEqual(gold_badge, ('Gold', 1000))
        self.assertLessEqual(gold_badge, ('Gold', 9999))

        platinum_badge = User.BADGE[1]
        self.assertGreaterEqual(platinum_badge, ('Platinum', 10000))
        self.assertLessEqual(platinum_badge, ('Platinum', 99999))

        diamond_badge = User.BADGE[0]
        self.assertGreaterEqual(diamond_badge, ('Diamond', 100000))

    # gender should be one fo the following corresponding values(MALE,FEMALE, OTHER) with its associated numerical
    # values(1, 2, 9)
    def test_gender_enum(self):
        expected_genders = ((2, "Male"), (1, "Female"), (9, "Other"))
        self.assertEqual(expected_genders, User_Profile.GENDER)
