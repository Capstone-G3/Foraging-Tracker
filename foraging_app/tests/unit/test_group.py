from django.test import TestCase
from unittest.mock import Mock


class TestGroupModel(TestCase):
    # def setUp(self):
    
        # self.mock_group = Mock()
        
        # self.test_group2 = Group.create(id=1234, category='Mushroom', name='Group3', description='',
        #                                 user_admin=self.test_user1.ID)
        # self.test_group = models.Group(id=8342, category='Mushrooms', name='Bob''s'' Group', description='',
        #                                user_admin=self.test_user1.ID)
        # self.test_user1_group = models.User_Group(user_id=self.test_user1.ID, group_id=self.test_group.ID,
        #                                           joined_date=date.today())
        # self.test_species = models.Species(id=7357, name='strawbery', category='Plant', description='', scope='berry',
        #                                    image='')



          #   test that Group ID is unique
    #   test that USER_ADMIN field is a valid ID associated to the Group admins ID


    # def test_group(self):
    #     self.assertEqual(self.test_group.user_admin, self.test_user1.ID)
    #     with self.assertRaises(AssertionError):
    #         Group.create(id=1234, category='Fishing', name='Group5', description='', user_admin=self.test_user1.id)
        
    #   test user group model's User ID corresponds to an existing members User's ID
    #   test user group model's Group ID corresponds to an existing GROUP ID
    #   test validation of creation date is entered
    # def test_user_group(self):
    #     self.assertEqual(self.test_user1_group.USER_ID, self.test_user1.id)
    #     self.assertEqual(self.test_user1_group.ID, self.test_group.id)
    #     self.assertIsNotNone(models.User_Group.joined_date)



     #   test that Group ID is unique
    #   test that USER_ADMIN field is a valid ID associated to the Group admins ID
    # def test_group(self):
    #     self.assertEqual(self.test_group.user_admin, self.test_user1.ID)
    #     with self.assertRaises(AssertionError):
    #         Group.create(id=1234, category='Fishing', name='Group5', description='', user_admin=self.test_user1.id)


    #   test user group model's User ID corresponds to an existing members User's ID
    #   test user group model's Group ID corresponds to an existing GROUP ID
    #   test validation of creation date is entered
    # def test_user_group(self):
    #     self.assertEqual(self.test_user1_group.USER_ID, self.test_user1.id)
    #     self.assertEqual(self.test_user1_group.ID, self.test_group.id)
    #     self.assertIsNotNone(models.User_Group.joined_date)
        pass 



