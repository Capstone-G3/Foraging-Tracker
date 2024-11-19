from PIL import Image
from os import listdir
from os.path import join as path_join
from numpy import ndarray 
from detect.predict import NsfwDectector, DectectorStatus
from unittest import TestCase

class TestDectector(TestCase):
    test_dir = path_join('tests_package','test_data')
    
    def setUp(self):
        self.image_paths = []
        self.detector = NsfwDectector()
        for name in listdir(self.test_dir):
            self.image_paths.append(path_join(self.test_dir,name))

    def test_successful_locate_file_when_input_image_path(self):
        image_obj = Image.open(self.image_paths[0])
        print(self.image_paths[0])
        nd_image = self.detector.__process_image__(image_obj)
        self.assertTrue(isinstance(nd_image,ndarray))

    def test_sucessful_predict_file_when_input_safe_image(self):
        image_obj = Image.open(self.image_paths[0])
        result = self.detector.determine(image_obj=image_obj)
        self.assertEqual(DectectorStatus.SAFE, result)

    def test_successful_predict_file_when_input_unsafe_image(self):
        image_obj = Image.open(self.image_paths[2])
        result = self.detector.determine(image_obj=image_obj)
        self.assertEqual(DectectorStatus.UNSAFE, result)    

    def test_successful_predict_file_when_input_combination_image(self):
        image_obj = Image.open(self.image_paths[1])
        result = self.detector.determine(image_obj=image_obj)
        self.assertEqual(DectectorStatus.SAFE, result)

