from django.shortcuts import render

from cropandyield.service import forecast, loaddata
import pickle
from sklearn import preprocessing
import pandas as pd
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def predict(request):
    states,seasons,crops=loaddata()
    return render(request, 'predict.html', {"states":states,"seasons":seasons,"crops":crops})

def predictAction(request):

    df = pd.read_csv(PROJECT_DIR+"\\cropandyield\\Crop_recommendation.csv")
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit_transform(df['label'])
    mapping = dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))
    print(mapping)

    N = request.GET['N']
    P = request.GET['P']
    K = request.GET['K']
    temperature = request.GET['temperature']
    humidity = request.GET['humidity']
    ph = request.GET['ph']
    rainfall = request.GET['rainfall']

    rf = pickle.load(open(PROJECT_DIR+'\\cropandyield\\randomforest_model.pickle', 'rb'))
    testrec = [float(N), float(P), float(K), float(temperature), float(humidity), float(ph),float(rainfall)]
    print(testrec)
    result = rf.predict([testrec])
    print(result)

    crop=list(mapping.keys())[list(mapping.values()).index(result[0])]

    #===================================================================================================================

    State_Name = request.GET["State_Name"]
    Season = request.GET["Season"]
    Crop = request.GET["Crop"]
    Area = request.GET["Area"]

    result = forecast(State_Name, Season, Crop, Area)
    production =str(result)

    # ===================================================================================================================
    return render(request, 'result.html', {"output1":"Predicted Crop "+str(crop),"output2":"Estimated Yield is :"+str(production)})