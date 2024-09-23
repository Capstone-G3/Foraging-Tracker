from django.test import TestCase
from foraging_app import models
from datetime import date


class TestModels(TestCase):
    def setup(self):
        self.Test_User1 = User.create(ID=1234, USER_NAME='BobsFindings', PASSWORD=12345, RATING=0,
                                      BADGE=models.BADGE.BRONZE,
                                      CREATED_SINCE=date.today())

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
    #
    def test_user_profile(self):
        pass

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

    def test_gender_enum(self):
        expected_genders = 1, 2, 9
        self.assertEqual(expected_genders, models.GENDER)
        self.assertEqual(models.GENDER.MALE.value, 1)
        self.assertEqual(models.GENDER.MALE.value, 2)
        self.assertEqual(models.GENDER.MALE.value, 9)

    def test_status_enum(self):
        pass

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
