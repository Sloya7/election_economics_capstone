import pandas as pd 
import os 

# file locations used as reference during development



file = 'Data/presidents/US Presidential Election Results - ResultsByCandidate.csv'
candidate_df = pd.read_csv(file)


#remove unneccessary columns
def format_df(df):
    del_columns = ['HomeState', 'CandPartyAbbrev', 'PartyAbbrev','Vice President']
    for c in del_columns:
        if c in df.columns:
            df.drop(columns = c, axis =1, inplace = True)   
    
format_df(candidate_df)

#create dataframe for data parsing
winners_df = pd.DataFrame()

#loop to find only the top listed canidate, which is the winning canidate
for y in candidate_df.ElectionYear.unique():
    filtered_df = candidate_df[candidate_df.ElectionYear == y]
    winners_df = pd.concat([winners_df, filtered_df.iloc[0]], axis = 1, ignore_index= True)

#data needs transposed
president_df = winners_df.transpose()
print('President Winners Parsed')
