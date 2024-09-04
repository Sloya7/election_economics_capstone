from Cleaning_preprocessing.config import *

# file locations used as reference during development

file = 'Cleaning_preprocessing/Data/presidents/US Presidential Election Results - ResultsByCandidate.csv'
candidate_df = pd.read_csv(file)


#remove unneccessary columns
def format_df(df):
    del_columns = ['HomeState', 'CandPartyAbbrev', 'PartyAbbrev','Vice President', 'CandParty']
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

#change dtype of ElecVoteShare and PopVoteShare to floats
president_df['ElecVoteShare'] = president_df['ElecVoteShare'].str.strip('%').astype(float)
president_df['PopVoteShare'] = president_df['PopVoteShare'].str.strip('%').astype(float)

#change Incumbent to a binary number. 0 = N, 1 = Y
for index, l in enumerate(president_df['Incumbent?']):
    if president_df.loc[index,'Incumbent?'] == 'N':
        president_df.loc[index,'Incumbent?'] = 0
    else:
        president_df.loc[index,'Incumbent?'] = 1


president_df['PopularVote'] = president_df['PopularVote'].astype(str).replace(',','',regex=True)
president_df['ElectoralVotes'] = president_df['ElectoralVotes'].astype(str).replace(',','',regex=True)
president_df['PopularVote'] = pd.to_numeric(president_df['PopularVote'])
president_df['ElectoralVotes'] = pd.to_numeric(president_df['ElectoralVotes'])
    
president_df.to_csv('Cleaned_data/presidents', encoding='utf-8', index = False)
print('President Winners Parsed and Saved in Cleaned_data/presidents')
