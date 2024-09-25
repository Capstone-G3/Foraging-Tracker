from django.test import TestCase
from foraging_app import models
from datetime import date


class TestModels(TestCase):
    def setup(self):
        self.Test_User1 = User.create(ID=1234, USER_NAME='BobsFindings', PASSWORD=12345, RATING=0,
                                      BADGE=models.BADGE.BRONZE,
                                      CREATED_SINCE=date.today())
        self.Test_User2 = User.create(ID=4353, USER_NAME='AliceFindings', PASSWORD=23445, RATING=0,
                                      BADGE=models.BADGE.BRONZE,
                                      CREATED_SINCE=date.today())
        self.Test_User1_Profile = User_Profile.create(
            first_name='Bob', last_name='Smith',
            email='test@gmail.com', home_address='1234 pine',
            phone='414-123-456-7890', gender=1, ID=12345, USER=self.Test_User1
        )
        self.Test_Group2 = Group.create(ID=1234, CATEGORY='Mushroom', NAME='Group3', DESCRIPTION='',
                                        USER_ADMIN=self.Test_User1.ID)
        self.Test_Group = models.GROUP(ID=8342, CATEGORY='Mushrooms', NAME='Bob''s'' Group', DESCRIPTION='',
                                       USER_ADMIN=self.Test_User1.ID)
        self.Test_User1_Group = models.USER_GROUP(USER_ID=self.Test_User1.ID, GROUP_ID=self.Test_Group.ID,
                                                  JOINED_DATE=date.today())
        self.Test_Species = models.SPECIES(ID=7357, NAME='strawbery', CATEGORY='Plant', DESCRIPTION='', SCOPE='berry', IMAGE= '')

    #   created users fields should not be null/empty
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

    #   test user profile model has an existing User it's connected to
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

    #   test user group model's User ID corresponds to an existing members User's ID
    #   test user group model's Group ID corresponds to an existing GROUP ID
    #   test validation of creation date is entered
    def test_user_group(self):
        self.assertEqual(self.Test_User1_Group.USER_ID, self.Test_User1.ID)
        self.assertEqual(self.Test_User1_Group.ID, self.Test_Group.ID)
        self.assertIsNotNone(models.USER_GROUP.JOINED_DATE)

    #   test that Group ID is unique
    #   test that USER_ADMIN field is a valid ID associated to the Group admins ID
    def test_group(self):
        self.assertEqual(self.Test_Group.USER_ADMIN, self.Test_User1.ID)
        with self.assertRaises(AssertionError):
            Group.create(ID=1234, CATEGORY='Fishing', NAME='Group5', DESCRIPTION='', USER_ADMIN=self.Test_User1.ID)

    def test_user_marker(self):
        pass
    #  **** REMINDER TO BE COMPLETED LATER**** (species portion of model)
    #   test marker model's OWNER_USER field is the associated  ID of the User creating the marker
    #   test marker model's CREATED_AT, IS_PRIVATE field is not empty/null
    #   test marker model's IS_PRIVATE field is a boolean value
    #   test marker model's ID field is unique

    def test_marker(self):
        Test_Marker = models.Marker(ID=0000, TITLE='Lion''s mane', LATITUDE=43.07866235729638,
                                     LONGITUDE=-87.881974725981,
                                     CREATED_AT=date.today(), IS_PRIVATE=False, SPECIES= , OWNER_USER=self.Test_User1.ID)
        self.assertEqual(Test_Marker.OWNER_USER, self.Test_User1.ID)
        self.assertIsNotNone(Test_Marker.MARKER.CREATED_AT)
        self.assertIsNotNone(Test_Marker.MARKER.IS_PRIVATE)
        self.assertIsInstance(Test_Marker.MARKER.IS_PRIVATE, bool)
        with self.assertRaises(AssertionError):
            Marker.create(ID=0000, TITLE='Lion''s mane', LATITUDE= 43.07866235729638, LONGITUDE= -87.881974725981, CREATED_AT=date.today() ,IS_PRIVATE= False ,SPECIES= ,OWNER_USER=self.Test_User1.ID)

    #   test like counter is asociated to its corresponding marker and marker owner (ID)
    def test_like_count(self):
        Test_Marker = models.MARKER(ID=0000, TITLE='Lion''s mane', LATITUDE=43.07866235729638,
                                    LONGITUDE=-87.881974725981,
                                    CREATED_AT=date.today(), IS_PRIVATE=False, SPECIES='', OWNER_USER=self.Test_User1.ID)
        Test_like_Marker = models.LIKE_COUNT(MARKER_ID=Test_Marker.ID,USER_ID=Test_Marker.OWNER_USER)
        self.assertEqual(Test_like_Marker.MARKER_ID, Test_Marker.ID)
        self.assertEqual(Test_like_Marker.USER_ID, Test_Marker.OWNER_USER)
    #   test friend request has a valid sending user as well as recieving user
    #   test status of request is not empty/null
    #   test request date of request is not empty/null
    def test_friend_request(self):
        # friend1 = models.FRIEND(USER_A=self.Test_User1, USER_B=self.Test_User2, SAVED_DATE=date.today())
        friend_request1 = models.FRIEND_REQUEST(UID_SENDER=self.Test_User1, UID_RECIEVER=self.Test_User2, STATUS=models.STATUS.PENDING, REQUEST_DATE=date.today())
        self.assertEqual(friend_request1.UID_SENDER, self.Test_User1)
        self.assertEqual(friend_request1.UID_RECIEVER, self.Test_User2)
        self.assertIsNotNone(friend_request1.STATUS)
        self.assertIsNotNone(friend_request1.REQUEST_DATE)
    #   test friend model field user_a and user_b correspond to user and the user that was added as a friend
    def test_friend(self):
        friend1 = models.FRIEND(USER_A=self.Test_User1, USER_B=self.Test_User2, SAVED_DATE=date.today())
        self.assertEqual(friend1.USER_A, self.Test_User1)
        self.assertEqual(friend1.USER_B, self.Test_User2)
        self.assertIsNotNone(friend1.SAVED_DATE)

    #   test species model fields are not null/empty
    #   test species model fields that require a STRING type are instances of str
    def test_species(self):
        self.assertIsNotNone(models.SPECIES.ID)
        self.assertIsInstance(models.SPECIES.ID,str)
        self.assertIsNotNone(models.SPECIES.IMAGE)
        self.assertIsInstance(models.SPECIES.CATEGORY, str)
        self.assertIsInstance(models.SPECIES.SCOPE, str)




