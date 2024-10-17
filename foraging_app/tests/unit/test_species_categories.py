import tempfile
import imghdr
import os
from django.test import TestCase
from foraging_app.models import Species
from django.core.files.uploadedfile import SimpleUploadedFile

class TestSpeciesModel(TestCase):

    def setUp(self):
        # Create test species with different categories
        self.species1 = Species.objects.create(name='Lion', category='Mammal', scope='Global',
                                               description='King of the Jungle',
                                               image=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        self.species2 = Species.objects.create(name='Eagle', category='Bird', scope='Global',
                                               description='Majestic bird',
                                               image=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        self.species3 = Species.objects.create(name='Shark', category='Fish', scope='Ocean',
                                               description='Fierce predator',
                                               image=tempfile.NamedTemporaryFile(suffix=".jpg").name)

    def test_category_field_not_null(self):
        # Ensure the category field is not null
        self.assertIsNotNone(self.species1.category)
        self.assertIsNotNone(self.species2.category)
        self.assertIsNotNone(self.species3.category)

    def test_category_field_type(self):
        # Ensure the category field is of type str
        self.assertIsInstance(self.species1.category, str)
        self.assertIsInstance(self.species2.category, str)
        self.assertIsInstance(self.species3.category, str)

    def test_category_values(self):
        # Ensure the category values are correct
        self.assertEqual(self.species1.category, 'Mammal')
        self.assertEqual(self.species2.category, 'Bird')
        self.assertEqual(self.species3.category, 'Fish')

    def create_test_image(self):
        test_image_path = tempfile.NamedTemporaryFile(suffix=".jpg").name
        with open(test_image_path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n'
                    b'\x00\x00\x00\rIHDR'
                    b'\x00\x00\x00\x01'
                    b'\x00\x00\x00\x01'
                    b'\x08\x02\x00\x00\x00'
                    b'\xd2\xc5\xf5\x3d'
                    b'\x00\x00\x00\x0bIDAT'
                    b'x\x9c'
                    b'\x01\x00\x00\x00\x01'
                    b'\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00')

        with open(test_image_path, 'rb') as f:
            return SimpleUploadedFile(name='test_image.jpg', content=f.read(), content_type='image/jpeg')
