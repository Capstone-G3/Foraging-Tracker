from datetime import date

from django.test import TestCase

from foraging_app.models import friend, User


class TestFriendshipModel(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='User1', password=1200354, rating=0,
                                         created_since=date.today())
        self.user2 = User.objects.create(username='User2', password=12384324, rating=0,
                                         created_since=date.today())
        self.user3 = User.objects.create(username='User3', password=1545684324, rating=0,
                                         created_since=date.today())

    #   test friend request has a valid sending user as well as receiving user
    #   test status of request is not empty/null
    #   test request date of request is not empty/null
    def test_friend_request(self):
        # friend1 = models.FRIEND(USER_A=self.Test_User1, USER_B=self.Test_User2, SAVED_DATE=date.today())
        friend_request1 = friend.Friend_Request(uid_sender=self.user1, uid_receiver=self.user2,
                                                status=1, request_date=date.today())
        self.assertEqual(friend_request1.uid_sender, self.user1)
        self.assertEqual(friend_request1.uid_receiver, self.user2)
        self.assertIsNotNone(friend_request1.status)
        self.assertIsNotNone(friend_request1.request_date)
        self.assertEqual(friend_request1.status, 1)

    #   test friend model field user_a and user_b correspond to user and the user that was added as a friend
    def test_friend(self):
        friend1 = friend.Friend(user_a=self.user1, user_b=self.user2, friend_since=date.today())
        friend.Friend(user_a=self.user1, user_b=self.user3, friend_since=date.today())
        self.assertEqual(friend1.user_a, self.user1)
        self.assertEqual(friend1.user_b, self.user2)
        self.assertIsNotNone(friend1.friend_since)
        self.assertEqual(friend1.friend_since, date.today())

        friends = friend.Friend.get_friends(self.user1)
        self.assertEqual(len(friends), 2)

    def test_friendship(self):
        friend_request1 = friend.Friend_Request(uid_sender=self.user1, uid_receiver=self.user2,
                                                status=1, request_date=date.today())
        self.assertEqual(friend_request1.status, 1)
        friend_request1.status = 2
        self.assertEqual(friend_request1.status, 2)
