from model_inspections import *
from saved_ML_models import *
from Create_ML.test_ML import num_models, model_names, model_dir


""" 
REFERENCE SAMPLE PACKAGE SETUP: 
silver_ML_package = [sil_X_train, sil_X_val, sil_X_test, sil_y_train, sil_y_val, sil_y_test]
"""

    
""" def get_importance(model_file, package): """
model_file = joblib.load('saved_ML_models/silver.pkl')
#name variables
model = model_file[0]
package = model_file[1]



for ec in package[1].Year.unique():
    print(ec)