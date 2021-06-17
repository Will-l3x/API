from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
import joblib
import requests
import json
from sklearn.preprocessing import LabelEncoder

class Predictor:
    def yields(self,State, Crop, Region, Area,  ):
        a = State
        b = Crop
        c = Region
        d = Area

        le = LabelEncoder()
        s_State = le.fit_transform([a])
        s_Crop = le.fit_transform([b])
        
        s_Area = le.fit_transform([d])

        model = joblib.load('yield-predictor.joblib')
        predictions = model.predict([[Region, Area, s_State, s_Crop, 8]])
        return predictions
    
    def cropsuggestion(self, Region, District, Season):
        ##  here the model suggest crops based on the location and season \

        a = District
        b = Season
        le = LabelEncoder()
        s_District = le.fit_transform([a])
        s_Season = le.fit_transform([b])

        model = joblib.load('crop-recommender.joblib')
        predictions = model.predict([[Region, s_District, s_Season]])
        
        return predictions

    def capitalpredictions(self, crop, area, yields):
        ## the model predicts the financial vaibility of the project

        return True




#Instantiate the node
app = Flask(__name__)

#Instantiate the predictor
predictor = Predictor()

#application routes
@app.route('/predict', methods=['Post'])
def new_prediction():
     values = request.get_json()
    #check that all required values of the post data are found
     required = ['Region', 'State', 'Crop', 'Area']
     if not all(k in values for k in required):
        return 'Missing values', 400

     data = predictor.yields(values['State'], values['Crop'], values['Region'], values['Area'])
     response = {'message':f'the yield predicted will be around: {data}'}
     return jsonify(response), 201

@app.route('/predictcrop', methods=['Post'])
def new_cropprediction():
     values = request.get_json()
    #check that all required values of the post data are found
     required = ['Region', 'District', 'Season']
     if not all(k in values for k in required):
        return 'Missing values', 400

     data = predictor.cropsuggestion(values['Region'], values['District'], values['Season'])
     response = {'message':f'with the input given the crop to plant would be {data}'}
     return jsonify(response), 201
    
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)