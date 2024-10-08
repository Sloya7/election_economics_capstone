from Model_inspections import *
from saved_ML_models import *
from Create_ML.test_ML import *


""" 
REFERENCE SAMPLE PACKAGE SETUP: 
silver_ML_package = [sil_X_train, sil_X_val, sil_X_test, sil_y_train, sil_y_val, sil_y_test]
"""

    
def find_importance():
    #loops for each model file name
    for name in model_names:
            #create the string path for pkl file
            model_path = '/'.join([model_dir,name +'.pkl'])
            #load file in
            model_package = joblib.load(model_path)
            
            #the file is a dictionary so assign what is the model and what is the data package
            model = model_package[0]
            package = model_package[1]   
                     
            #use the test datasubset to run the permutation inspection
            time_importance = pi(model,package[2] , package[5], n_repeats = 20, random_state=42)
            #create dataframe that housed the mean results and the stand_deviattions
            importance_df = pd.DataFrame({'importance_mean': time_importance['importances_mean'],'importance_std': time_importance['importances_std']}, index= model.feature_names_in_)
            
            #provide visual of data
            print('\n', name, 'feature importance:', '\n', importance_df)
    return  


find_importance()



