""" Here we get to tune a Random Forest Classifer using Grid Search. 
Models are saved in a dictionary in the format of {'model name': model}
where the model name refers to the type of data ie-gold, silver, market

REFERENCE SAMPLE PACKAGE SETUP: 
silver_ML_package = [sil_X_train, sil_X_val, sil_X_test, sil_y_train, sil_y_val, sil_y_test]


"""
from Create_ML.ML_config import *
from Create_ML.binarizer_and_split import silver_ML_package, gold_ML_package, market_ML_package
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import joblib 

#makeing the classifier
clf = RandomForestClassifier()


#data to be processed and where it will be saved
packages = [silver_ML_package, gold_ML_package, market_ML_package]
best_models = {}
model_dir = '/home/sloya7/miniconda3/election_economics_capstone/saved_ML_models'

#tested parameters
param_grid = {
    'n_estimators' : [5,10,25,50,75],
    'max_depth' : [1,5,10,25,50],
    'min_samples_split' : [2,5,10,20],
    'min_samples_leaf' : [1,5,10,25],
}



def find_parameters(package):
    #creates string name for the package to reference in best_models dictionary
    if package is market_ML_package:
        package_name = 'market'
    if package is gold_ML_package:
        package_name = 'gold'
    if package is silver_ML_package:
        package_name = 'silver'
        
    #output to track progress
    print('Starting', package_name, 'parameter testing.')
    s_time = time.time()
    
    """ for array in package:
        print(array.head()) """
    
    #defines the RandomForestClassifier using the packages '_X_train' and package '_y_train' data
    package_clf = clf.fit(package[0], package[3])
    
    #creates and fits the grid serch for specific package
    param_search = GridSearchCV(package_clf, param_grid, cv = 4, scoring='accuracy')
    param_search.fit(package[0], package[3])
    
    #used for resource management and tuning
    e_time = time.time()
    print('Parameter Testing Took:', format(e_time - s_time,'.2f'))

    accurate_model = param_search.best_estimator_
 
    print("Accuracy of model:", param_search.best_score_)
    
    best_models[package_name] = [accurate_model, package]
    
    ### Saving the Model ###
    
    #create string that joins directory, name plus extension
    trained_model_path = '/'.join([model_dir,package_name + '.pkl'])
    
    #save the model in the file location above
    joblib.dump(best_models[package_name], trained_model_path)
    print(f"Model {package_name} saved")
    
    
    
    return 

for package in packages:
    find_parameters(package)



