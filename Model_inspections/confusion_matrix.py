from Model_inspections.__init__ import *
from saved_ML_models import *
from Model_inspections.feature_inspections import *
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

for name in model_names:
        #create the string path for pkl file
        model_path = '/'.join([model_dir,name +'.pkl'])
        model_package = joblib.load(model_path)
        
        #the file is a dictionary so assign what is the model and what is the data package
        model = model_package[0]
        package = model_package[1]   

        preds = model.predict(package[2])
        
        con_mat = confusion_matrix(package[5],preds)

        graph = ConfusionMatrixDisplay(confusion_matrix=con_mat)

        graph.plot()
        plt.title(name, "preditions")
        plt.show()
        
        
        
        