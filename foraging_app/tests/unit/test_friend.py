from django.test import TestCase
from unittest.mock import Mock

class TestFriendshipModel(TestCase):
    
    #   test friend request has a valid sending user as well as receiving user
    #   test status of request is not empty/null
    #   test request date of request is not empty/null
    # def test_friend_request(self):
    #     # friend1 = models.FRIEND(USER_A=self.Test_User1, USER_B=self.Test_User2, SAVED_DATE=date.today())
    #     friend_request1 = models.Friend_Request(uid_sender=self.test_user1, uid_reciever=self.test_user2,
    #                                             STATUS=models.Status.pending, REQUEST_DATE=date.today())
    #     self.assertEqual(friend_request1.uid_sender, self.test_user1)
    #     self.assertEqual(friend_request1.uid_reciever, self.test_user2)
    #     self.assertIsNotNone(friend_request1.status)
    #     self.assertIsNotNone(friend_request1.request_date)


    
    #   test friend model field user_a and user_b correspond to user and the user that was added as a friend
    # def test_friend(self):
    #     friend1 = models.Friend(user_a=self.test_user1, user_b=self.test_user2, saved_date=date.today())
    #     self.assertEqual(friend1.user_a, self.test_user1)
    #     self.assertEqual(friend1.user_b, self.test_user2)
    #     self.assertIsNotNone(friend1.saved_date)
    pass
