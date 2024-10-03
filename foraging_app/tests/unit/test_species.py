from django.test import TestCase
from unittest.mock import Mock
import os
import tempfile
import imghdr


class TestSpeciesModel(TestCase):

    # def setUp(self):
    #     self.test_species = models.Species(id=7357,
    #                                        name='strawbery',
    #                                        category='Plant',
    #                                        description='',
    #                                        scope='berry',
    #                                        image='')


    #   test species model fields are not null/empty
    #   test species model field type is an image
    #   test species model fields that require a STRING type are instances of str.
    # def test_species(self):
    #     self.assertIsNotNone(models.Species.id)
    #     self.assertIsInstance(models.Species.id, str)
    #     self.assertIsNotNone(models.Species.image)
    #     self.assertIsInstance(models.Species.category, str)
    #     self.assertIsInstance(models.Species.scope, str)
    #     testImagePath = tempfile.NamedTemporaryFile(suffix=".jpg").name
    #     # 1x1 black pixel image
    #     with open(testImagePath, 'wb') as f:
    #         f.write(b'\x89PNG\r\n\x1a\n'
    #                 b'\x00\x00\x00\rIHDR'
    #                 b'\x00\x00\x00\x01'
    #                 b'\x00\x00\x00\x01'
    #                 b'\x08\x02\x00\x00\x00'
    #                 b'\xd2\xc5\xf5\x3d'
    #                 b'\x00\x00\x00\x0bIDAT'
    #                 b'x\x9c'
    #                 b'\x01\x00\x00\x00\x01'
    #                 b'\x00\x00\x00\x00'
    #                 b'\x00\x00\x00\x00')
    #     models.Species.Image = testImagePath
    #     imageType = imghdr.what(models.Species.Image)
    #     self.assertIsNotNone(imageType)
    #     os.remove(testImagePath)
    pass