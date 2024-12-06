from os.path import join as path_join
from PIL import Image
from tensorflow import keras
import numpy as np
from enum import Enum

class DectectorStatus(Enum):
    """
        A simple way to represent Determined Status, can always be changed to binaries or keep it as String. 
    """
    SAFE = "Safe"
    UNSAFE = "Unsafe"

class NsfwDectector:
    __categories = ['drawing', 'hentai', 'neutral', 'porn', 'sexy']
    
    def __init__(self):
        model_path = path_join('detect', 'model', 'nsfw_inception3.h5')
        self._model = keras.models.load_model(model_path, compile=False) # Using static model
        self._img_size = (299,299) #Inception 3 use 299 and MobileNetV2 use 224

    def __process_image__(self, image_obj):
        """
        Before uses for prediction, the Image must be processed with numpy first.
        The model must be able to "view" the Image in an internal structured.

        Args:
            image_obj (PIL.Image.Image): Loaded image object

        Raises:
            ValueError: The input is not an Image Object, therefore it can not process

        Returns:
            numpy.ndarray: The returned is a matrix representation of the processed image for prediction.
        """

        if not isinstance(image_obj, Image.Image):
            raise ValueError("The Input Object is not an Image.")
        
        # Prevent Alpha Channel (Shape only expecting Red-Green-Blue)
        if image_obj.mode != 'RGB':
            image_obj = image_obj.convert('RGB')
        image = image_obj.resize(size=self._img_size)
        image = keras.preprocessing.image.img_to_array(image)
        image /= 255
        return np.asarray([image]) # Extended a single dimension due to matrix (None, 299, 299, 3) Model.
    
    def determine(self, image_obj):
        """
        Instead of scoring the input image from path, this function will determine if input image is good to be save and display
        on the website for other users.

        Args:
            image_obj (PIL Image.Image): Loaded Image as Object.

        Returns:
            DetectorStatus: An enum that determine the returned value of Safe or Unsafe.
        """
        nd_image = self.__process_image__(image_obj)
        predictions = self._model.predict(nd_image)

        prediction_tagged = {}
        for i,prediction in enumerate(predictions[0]):
            prediction_tagged[self.__categories[i]] = float(prediction)
        
        unsafe_categories = ['hentai', 'porn', 'sexy']
        safe_threshold = prediction_tagged['neutral'] + prediction_tagged['drawing'] # Talk over with group.
        unsafe_threshold = 0
        for key in unsafe_categories:
            unsafe_threshold = prediction_tagged[key] + unsafe_threshold
        
        if unsafe_threshold > safe_threshold:
            return DectectorStatus.UNSAFE

        return DectectorStatus.SAFE

        
        

    


    

    
