from flask import Flask, request, redirect, url_for, jsonify
from flask_restful import Resource, Api
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import base64


app = Flask(__name__)
api = Api(app)

CORS(app)

model = load_model('model.h5')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Prediction(Resource):
    def post(self):
        image = request.files['file']
        print(type(image))
        #prediction = model.predict(image)
        #return {'result': prediction}
        return "I got image"

@app.route("/yo", methods=['POST'])
def make_predictions():
    try:
        content = request.get_json(force=True)
    except HTTPException as e:
        return jsonify({'error': 'Request data invalid'}), 400
    
    return jsonify({'prediction': 'heheh'})

api.add_resource(HelloWorld, '/')
api.add_resource(Prediction, '/predict')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

