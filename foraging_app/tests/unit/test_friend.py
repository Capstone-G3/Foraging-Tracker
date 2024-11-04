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

        self.friend1 = friend.Friend.objects.create(user=self.user1)
        self.friend2 = friend.Friend.objects.create(user=self.user2)
        self.friend3 = friend.Friend.objects.create(user=self.user3)
        self.friend_request = friend.Friend_Request(uid_sender=self.user2, uid_receiver=self.user1,
                                                    status=1, request_date=date.today())

    #   test friend request has a valid sending user as well as receiving user
    #   test status of request is not empty/null on default
    #   test request date of request is not empty/null
    def test_friend_request(self):
        friend_request1 = friend.Friend_Request(uid_sender=self.user1, uid_receiver=self.user2,
                                                request_date=date.today())
        self.assertEqual(friend_request1.uid_sender, self.user1)
        self.assertEqual(friend_request1.uid_receiver, self.user2)
        self.assertIsNotNone(friend_request1.status)
        self.assertIsNotNone(friend_request1.request_date)
        self.assertEqual(friend_request1.status, 1)

    #   test friend model function add_friend(), correctly adds user 2 into user 1's friends list
    def test_add_friend(self):
        self.friend1.add_friend(self.user2)
        self.assertIn(self.user2, self.friend1.friends.all())

    #   test friend model function remove_friend(), removes user 2 from user 1's friends list
    def test_remove_friend(self):
        self.friend2.add_friend(self.user1)
        self.friend1.remove_friend(self.user2)
        self.assertNotIn(self.user2, self.friend1.friends.all())

    # test friend model function unfriend removes user 2 from user 1's friend's list, as well as user 1 from user 2's -
    # friends list
    def test_unfriend(self):
        self.friend1.add_friend(self.user2)
        self.friend2.add_friend(self.user1)
        self.friend1.unfriend(self.user2)
        self.assertNotIn(self.user2, self.friend1.friends.all())
        self.assertNotIn(self.user1, self.friend2.friends.all())

    # test friend model function is_friend() returns True if user 2 is in user 1's friends list after being added,
    # and vice versa. PRE CHECK is_friend() returns False for user 2 being in user 1's friend's list before
    # being added as a friend and vice versa
    def test_is_friend(self):
        self.assertFalse(self.friend1.is_friend(self.user2))

        self.friend1.add_friend(self.user2)
        self.assertTrue(self.friend1.is_friend(self.user2))

        self.assertFalse(self.friend2.is_friend(self.user1))

        self.friend2.add_friend(self.user1)
        self.assertTrue(self.friend2.is_friend(self.user1))

    # test friend_request model's function accept() adds sender to receiver's friends list.
    # test friend_request model field status updates accordingly when a user (user1) accepts a friend
    # request from a sender (user2).
    def test_accept_friend_request(self):
        self.assertEqual(self.friend_request.status, 1)

        isAccepted = self.friend_request.accept()
        self.assertEqual(isAccepted, True)
        self.assertEqual(self.friend_request.status, 0)

        self.assertIn(self.user2, self.friend1.friends.all())

    # test friend_request model function reject() sets status to 2.
    # test reject() in fact does indeed not add sender (user1) to receiver's (user1)  friends list
    def test_reject_friend_request(self):
        self.assertEqual(self.friend_request.status, 1)

        self.friend_request.reject()
        self.assertEqual(self.friend_request.status, 2)

        self.assertNotIn(self.user2, self.friend1.friends.all())
