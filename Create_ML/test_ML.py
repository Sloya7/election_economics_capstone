""" 
This file checks to see if models have been trained and saved. It then taked the model and applies
the test data subset and provides the score for the gold, silver and market database.
"""


from Create_ML.ML_config import *
from sklearn.ensemble import RandomForestClassifier
import joblib

""" 
REFERENCE SAMPLE PACKAGE SETUP: 
silver_ML_package = [sil_X_train, sil_X_val, sil_X_test, sil_y_train, sil_y_val, sil_y_test]
"""

model_dir = '/home/sloya7/miniconda3/election_economics_capstone/saved_ML_models/'
#finds number of files in the directory
num_models = len([name for name in os.listdir(model_dir) if os.path.isfile(os.path.join(model_dir, name))])


#hard coded extensions since they are known. Could be 
#dynamically coded if project is expanded
model_names = ['gold', 'silver', 'market']

#takes model and package list to score the model
def score_ML(model, package):
    X_data = package[2]
    y = package[5]
    score = model.score(X_data, y)
    return score

#loops through files and provides data to score_ML
def test_ML():
    for name in model_names:
            model_path = '/'.join([model_dir,name +'.pkl'])
            model = joblib.load(model_path)
            score = score_ML(model[0],model[1])
            print(name, 'scored:', score)
    return   


# tests the models have been trained. If not, will call the training file first
if num_models >= 2:
    test_ML()
    
else:
    with open('/home/sloya7/miniconda3/election_economics_capstone/Create_ML/train_ML.py') as f:
        exec(f.read())
    test_ML()
    