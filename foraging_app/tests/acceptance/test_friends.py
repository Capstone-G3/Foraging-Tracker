from datetime import datetime

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from foraging_app.models import User
from foraging_app.models.user import User_Profile
from foraging_app.models.friend import Friend
from foraging_app.models.friend import Friend_Request


class FriendsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create_user(username="user1",
                                              password="111",
                                              email="user1@gmail.com")

        User_Profile.objects.create(home_address="111 St",
                                    phone="123-456-7899",
                                    gender=1,
                                    user_id=self.user1)

        self.user2 = User.objects.create_user(username="user2",
                                              password="111",
                                              email="user2@gmail.com")

        User_Profile.objects.create(home_address="111 St",
                                    phone="123-456-7899",
                                    gender=2,
                                    user_id=self.user2)

        self.user3 = User.objects.create_user(username="user3",
                                              password="111",
                                              email="user3@gmail.com")

        User_Profile.objects.create(home_address="111 St",
                                    phone="123-456-7899",
                                    gender=0,
                                    user_id=self.user3)

        Friend.objects.create(user_a=self.user1, user_br=self.user2, friend_since=datetime.now())
        Friend.objects.create(user_a=self.user1, user_br=self.user3, friend_since=datetime.now())
        Friend_Request.objects.create(uid_sender=self.user2, uid_receiver=self.user1, status=1,
                                      request_date=datetime.now())
        Friend_Request.objects.create(uid_sender=self.user3, uid_receiver=self.user1, status=1,
                                      request_date=datetime.now())

        self.client.login(username=self.user1.username, password=self.user1.password)

    # test that user profile displays friend count
    def test_friend_count(self):
        response = self.client.get(reverse('profile', args=self.user1.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Friends: 2')

    # test that friends page displays currently added friends
    def test_display_friends(self):
        response = self.client.get(reverse('friends', args=self.user1.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, self.user3.username)

    # test that friends page displays updated friends list after removing a friend
    def test_removed_friends(self):
        Friend.objects.delete(self.user1, self.user3)
        # Friend.remove(self.user1, self.user3)
        response = self.client.get(reverse('friends'), args=self.user1.id)
        self.assertContains(response, self.user2.username)
        self.assertNotContains(response, self.user3.username)

    # test that friends count on user profile correctly updates upon removing a friend
    def test_removed_friends_count(self):
        Friend.objects.delete(self.user1, self.user3)
        # Friend.remove(self.user1, self.user3)
        response = self.client.get(reverse('profile', args=self.user1.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Friends: 1')

    # test when user clicks on a friend in their friend page they are redirected to that friends profile page
    def test_friend_redirect(self):
        self.client.get(reverse('friends', args=self.user1.id))

        response = self.client.get(reverse('profile', args=[self.user2.id]))

        self.assertRedirects(response, reverse('profile', args=self.user2.id))
