import tensorflow as tf
import PIL
import cv2
import tensorflow_hub as hub
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()


 
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


class Model:
    def __init__(self):
        self.model = None
        
    def load(self, path):
        self.model = tf.keras.models.load_model(path, custom_objects={'KerasLayer': hub.KerasLayer})
        
    def process_image(self, image_file):
        image = PIL.Image.open(image_file)
        image_array = tf.keras.preprocessing.image.img_to_array(image)
        image_array = tf.image.resize(image_array, [224, 224]) / 255
        image_array = tf.expand_dims(image_array, axis=0)
        return image_array
    
    def predict(self, image_array):
        return self.model.predict(image_array)
    
    def predicted_class(self, predictions):
        return tf.argmax(predictions, axis=1)
    
    def confidence(self, predictions):
        probabilities = tf.nn.softmax(predictions).numpy()
        confidence = tf.reduce_max(probabilities) * 100
        return confidence