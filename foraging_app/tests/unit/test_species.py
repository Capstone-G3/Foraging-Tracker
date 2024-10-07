from django.test import TestCase
import os
import tempfile


from foraging_app.models import Species


class TestSpeciesModel(TestCase):

    def setUp(self):
        pass

    def test_species(self):
        testImagePath = tempfile.NamedTemporaryFile(suffix=".png").name
        # 1x1 black pixel image
        with open(testImagePath, 'wb') as f:
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
        species1 = Species.objects.create(id=123, name='Species 1', category='fruit'
                                          , scope='testscope', description='Found berry', image=testImagePath)
        self.assertIsNotNone(species1.id)
        self.assertIsNotNone(species1.name)
        self.assertIsNotNone(species1.image)
        self.assertIsInstance(species1.category, str)
        self.assertIsInstance(species1.scope, str)
        os.remove(testImagePath)
