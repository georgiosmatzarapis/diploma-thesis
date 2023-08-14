import json
import os
from pprint import pprint

def file_path(folder_name, file_name):
    """ Specify file path. """
    file_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(file_directory)
    file_path = os.path.join(parent_directory, f'{folder_name}/{file_name}')
    return file_path


with open(file_path('twitter_api/files','symptoms.json')) as f:
    symptoms = json.load(f)

for symptom in symptoms:
    for symptomKey, valueSymptomList in symptom.items():
        print('Key: ' + symptomKey + ' - Value: ' + str(valueSymptomList))

        for symptomSubName in valueSymptomList:
            print("Checking symptom: " + symptomSubName)
        print()
        print()
