from flask import Flask, request, redirect, url_for
from flask_restful import Resource, Api
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model

app = Flask(__name__)
api = Api(app)

model = load_model('model.h5')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Prediction(Resource):
    def post(self):
        image = request.files['file']
        prediction = model.predict(image)
        return {'result': prediction}

api.add_resource(HelloWorld, '/')
api.add_resource(Prediction, '/predict')

if __name__ == '__main__':
    app.run(debug=True)

