from flask import Flask, request, redirect, url_for, jsonify
from flask_restful import Resource, Api
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import base64
import cv2
import numpy as np
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

app = Flask(__name__)
api = Api(app)

CORS(app)
model = load_model('modelv2.h5')
label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("demo/trained_labels.txt")]


def predict(image_data):

    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})

    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

    max_score = 0.0
    res = ''
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        if score > max_score:
            max_score = score
            res = human_string
    return res
    
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Prediction(Resource):
    def post(self):
        img_str = request.form['image']
        np_img = np.fromstring(img_str, np.uint8)
        print(np_img)
        img_arr = cv2.resize(np_img, dsize=(64, 64), interpolation=cv2.INTER_CUBIC)
        print(img_arr.shape)
        #img_arr = image.img_to_array(img)
        x = np.expand_dims(img_arr, axis=0)
        print(x.shape)
        x = preprocess_input(x)
        print(x)
        print(x.shape)
        prediction = model.predict(x, batch_size=1)
        print("HELLO")
        class_prediction = model.predict_classes(x, batch_size=1)
        print(prediction)
        print(class_prediction)
        return "I got image"

class Tensor(Resource):
    def post(self):
        img_str = request.form['image']
        #res = predict(img_str)
        return {'prediction': res}


@app.route("/yo", methods=['POST'])
def make_predictions():
    try:
        content = request.get_json(force=True)
    except HTTPException as e:
        return jsonify({'error': 'Request data invalid'}), 400
    
    return jsonify({'prediction': 'heheh'})

api.add_resource(HelloWorld, '/')
api.add_resource(Prediction, '/predict')
api.add_resource(Tensor, '/tensor')

if __name__ == '__main__':
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        app.run(debug=True, port=5000)

