from datetime import date

from django.db import IntegrityError
from django.test import TestCase
from unittest.mock import Mock

from foraging_app.models import User, Group
from foraging_app.models.group import User_Group


class TestGroupModel(TestCase):

    def setUp(self):
        pass
    #   test user group model's User ID corresponds to an existing members User's ID
    #   test user group model's Group ID corresponds to an existing GROUP ID
    def test_user_group(self):
        user1 = User.objects.create(id=5256, username='Bob', password='123', rating=0,
                                    created_since=date.today())
        test_group = Group.objects.create(id=8342, category='Mushrooms', name='BobGroup', description='',
                                          user_admin=user1)
        user1_group = User_Group.objects.create(user_id=user1, group_id=test_group)
        self.assertEqual(user1_group.user_id, user1)
        self.assertEqual(user1_group.group_id, test_group)

    #   test that Group ID is unique
    #   test that USER_ADMIN field is a valid ID associated to the Group admins ID
    def test_group(self):
        user1 = User.objects.create(id=5256, username='Bob', password='123', rating=0,
                                    created_since=date.today())
        test_group = Group.objects.create(id=8342, category='Mushrooms', name='BobGroup', description='',
                                          user_admin=user1)
        self.assertEqual(test_group.user_admin, user1)
        with self.assertRaises(IntegrityError):
            Group.objects.create(id=1234, category='Fishing', name='BobGroup', description='', user_admin=user1)


