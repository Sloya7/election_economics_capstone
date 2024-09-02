from model_inspections import *
from saved_ML_models import *
import matplotlib.pyplot as plt


""" 
REFERENCE SAMPLE PACKAGE SETUP: 
silver_ML_package = [sil_X_train, sil_X_val, sil_X_test, sil_y_train, sil_y_val, sil_y_test]
"""

    
""" def get_importance(model_file, package): """
model_file = joblib.load('saved_ML_models/market.pkl')
#name variables
model = model_file[0]
package = model_file[1]

#call permutaion influence method
feature_influence = pi(model, package[2], package[5], n_repeats = 5, random_state=42)

importance_df = pd.DataFrame({'importance_mean': feature_influence['importances_mean'],'importance_std': feature_influence['importances_std']}, index= model.feature_names_in_)


#sorted_importances =importance.sort_values(by = 'ElectCycle', ascending=False)
print(importance_df) 
    
"""     return something """



#TODO getting an array of 0s
