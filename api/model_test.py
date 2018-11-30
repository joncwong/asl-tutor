import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import numpy as np
import cv2

if __name__ == '__main__':
    image_path = "/Users/jon/documents/asl-tutor/data/asl_alphabet_test/rsz_1l-real-test-flip.jpg"

    test_image= image.load_img(image_path,target_size = (64, 64))
    model = load_model('modelv2.h5')
    model.summary()
    test_image = image.img_to_array(test_image)
    x = np.expand_dims(test_image, axis=0)
    x = preprocess_input(x)
    print(x)
    prediction = model.predict(x, batch_size=1)
    class_prediction = model.predict_classes(x, batch_size=1)
    print(prediction)
    print(class_prediction)
    #y_classes = keras.np_utils.probas_to_classes(prediction)
