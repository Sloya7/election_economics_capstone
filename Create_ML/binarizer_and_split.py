""" This file pulls the coding from the preprocessing and check if it has already been preprocessed. If the 
data needs processing it, it does so. 
It then combines the data to develop numeric binary data for the 
appropriate fields. 
It then seperates the data back out into the different minerals and the market information.
This is done to make sure we can differentiate the performance of each compared to ElectionCycles and one trait
does not overshadow other influences.
After seperation, the dataframes are cleaned of non nuermic data and seperated into X and y training and testing sets.

The lists are packaged together into an array for easier importing into next file"""


from Create_ML.ML_config import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from Create_ML.assemble_data import combine_data
pd.set_option('future.no_silent_downcasting', True)

# creates the combined dataframe
combined_data = combine_data()

#correct the type of Electcycle
combined_data.Asset_name = combined_data.Asset_name.astype(str)

#replace values to transform 'PriorYear', 'ElectYear', 'Year1', 'Year2', 'Gain', 'Loss' to binary

bin_columns = ['PriorYear','ElectYear', 'Year1', 'Year2', 'Gain', 'Loss']

for c in bin_columns:
    combined_data[c] = combined_data[c].replace({True: 1, False: 0, 'yes': 1, 'no' : 0}).astype(int)

# since prep for the ML is complete, seperate out the minerals vs market info for independent ML application
silver_ML_data = combined_data[combined_data['Asset_name'] == 'silver_price']
gold_ML_data = combined_data[combined_data['Asset_name'] == 'gold_price']
market_ML_data = combined_data[~combined_data['Asset_name'].isin(['gold_price', 'silver_price'])]

ML_data_list = [silver_ML_data, gold_ML_data, market_ML_data]

X_list = {}
y_list = {}

#create the X and y data for the mineral in else case. Markets take a special approach in the 'if' case
for df in ML_data_list:
    if df is market_ML_data:
        asset_name = 'market'
        
    else:
        #find assets str name
        asset_name = df.iloc[2,1]
        
    #remove the last non numeric column
    df.drop(columns = 'Asset_name', axis =1, inplace=True)

    # create target value
    y_list[asset_name] = df['Gain']

    # create remainder of values    
    X_list[asset_name] = df.drop(columns = ['Gain'], axis = 1)
    
print(X_list.keys())

#create train and test sample for X and y of each dataframe

sil_X_train, sil_X_test, sil_y_train, sil_y_test = train_test_split(X_list['silver_price'],y_list['silver_price'] , random_state=42)

gold_X_train, gold_X_test, gold_y_train, gold_y_test = train_test_split(X_list['gold_price'],y_list['gold_price'], random_state=42)

market_X_train, market_X_test, market_y_train, market_y_test = train_test_split(X_list['market'],y_list['market'], random_state=42)

silver_ML_package = [sil_X_train, sil_X_test, sil_y_train, sil_y_test]
gold_ML_package = [gold_X_train, gold_X_test, gold_y_train, gold_y_test]
market_ML_package = [market_X_train, market_X_test, market_y_train, market_y_test]