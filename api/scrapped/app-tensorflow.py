from flask import Flask, request, redirect, url_for
from flask_restful import Resource, Api
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import numpy as np
import cv2

app = Flask(__name__)
api = Api(app)

model = load_model('modelv2.h5')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Prediction(Resource):
    def post(self):
        img_str = request.files['file'].read()
        print(type(img_str))
        np_img = np.fromstring(img_str, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        img_arr = cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_CUBIC)
        #img_arr = image.img_to_array(img)
        x = np.expand_dims(img_arr, axis=0)
        x = preprocess_input(x)
        print(x.shape)
        prediction = model.predict(x, batch_size=1)
        print("HELLO")
        class_prediction = model.predict_classes(x, batch_size=1)
        print(prediction)
        print(class_prediction)
        return "I got image"

api.add_resource(HelloWorld, '/')
api.add_resource(Prediction, '/predict')

if __name__ == '__main__':
    app.run(debug=True)

