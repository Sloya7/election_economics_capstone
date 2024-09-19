This project is designed to run a machine learning Random Forest Classifier on mineral, market and presidential data. The input is CSV data that is cleaned and preprocessed. The output is 3 seperate models that predict whether that election year will result in a price 'gain'. A 'gain' is currently defined as a value that is at or above the 80th quantile.

As this project expands, pay close attention to which branch you are viewing from as new approaches to the data may change the target from 'gain' to 'loss' or another variable. 

Dependencies are listed inside the dependencies.txt file and are the most current version of all packages at the time of the project(September 2024).

Once the project is loaded, the files are designed to cascade into each other. For example, running Create_ML.test_ML.py will automactically check that the cleaning and preprocessing steps are completed and if not completed, run the appropriate scripts. 

To reach the target analysis, run the one of the following code: 
Model_inspections.feature_inspections.py
Create_ML.test_ML.py
or using the 
python -m Create_ML.test_ML
python -m Model_inspections.feature_inspections
codings. 

If you want to print the graphs using python files, the confusion_matrix and data_distro files will do so. You also may use the 'project_visuals' Jupyter Notebook to see all the visual in one place. 
