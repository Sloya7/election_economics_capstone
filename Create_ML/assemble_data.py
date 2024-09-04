"""This file defines the function that is used to assemble the 3 sources of data. It also used the presidential database as a reference point to create 
relationships between the market and mineral data"""


"""TODO: add the incubant column?"""

from Create_ML.ML_config import *

def combine_data():

    #checks for preprocessed files and processed them if needed
    csv_names = {'markets.csv': 'Cleaning_preprocessing/ETF_preprocessing/etf_preprocessing.py',
             'presidents.csv': 'Cleaning_preprocessing/President_preprocessing/president_preprocessing.py', 
             'minerals.csv': 'Cleaning_preprocessing/Mineral_preprocessing/mineral_preprocessing.py'}
    for n in csv_names:
        print('Checking for file', n)
        if os.path.exists('Cleaned_data/'+n):
            print(n, 'exists.')
            continue
        else:
            with open(csv_names[n]) as f:
                exec(f.read())
                
    print('\n',
        'Preprocessing Complete!')
     
     
     
    #file locations
    president_df = pd.read_csv('Cleaned_data/presidents.csv')
    mineral_df = pd.read_csv('Cleaned_data/minerals.csv')
    market_df = pd.read_csv('Cleaned_data/markets.csv')
        
    # Combines the markets and mineral dataframes 
    money_df = pd.concat([mineral_df, market_df], axis=0, ignore_index=True)
    
    # Initialize lists for storing prior and future years related to election years
    prior_years = []
    year1_list = []
    year2_list = []
    
    # Extract unique election years from the president_df
    election_years = president_df.ElectionYear.unique()

    # Loop through each election year to populate prior and future year lists
    for y in election_years:
        prior_years.append(y - 1)
        year1_list.append(y + 1)
        year2_list.append(y + 2)
       

    ### Create new columns to establish a relationship between election years and market data
    
    #new columns
    money_df['ElectCycle'] = int
    money_df['PriorYear'] = bool
    money_df['ElectYear'] = bool
    money_df['Year1'] = bool
    money_df['Year2'] = bool
    
    #imported data from presidents
    money_df['Incumbent'] = int
    money_df['PopVoteShare'] = float
    money_df['ElecVoteShare'] = float



    #assigns a boolan values for where in the election cycle a year is located
    money_df.loc[:,'ElectYear'] = money_df['Year'].isin(election_years)
    money_df.loc[:,'PriorYear'] = money_df['Year'].isin(prior_years)
    money_df.loc[:,'Year1'] = money_df['Year'].isin(year1_list)
    money_df.loc[:,'Year2'] = money_df['Year'].isin(year2_list)

    #enumerates over the money_df to assign which election cycle a specific instance belongs to 
    for index, y in enumerate(money_df.Year):
        
        year_to_test = money_df.loc[index, 'Year']
        
        if year_to_test % 4 == 3:
            money_df.loc[index,'ElectCycle'] = year_to_test + 1
        elif year_to_test % 4 == 1:
            money_df.loc[index,'ElectCycle'] = year_to_test - 1
        elif year_to_test % 4 == 2:
            money_df.loc[index,'ElectCycle'] = year_to_test - 2
        elif year_to_test % 4 == 0:
            money_df.loc[index,'ElectCycle'] = year_to_test
          
    #fills election related values based on the election year column
    for index, c in enumerate(money_df['ElectCycle']):
        for y in election_years:
            if c == y:
                money_df.loc[index,'Incumbent'] = president_df[president_df['ElectionYear'] == y]['Incumbent?'].values[0]
                money_df.loc[index,'PopVoteShare'] = president_df[president_df['ElectionYear'] == y]['PopVoteShare'].values[0]
                money_df.loc[index,'ElecVoteShare'] = president_df[president_df['ElectionYear'] == y]['ElecVoteShare'].values[0]

      
    drop_cols = ['Year_Open', 'Year_Close', 'Year_Change', 'Loss','Year']
    money_df = money_df.drop(columns = drop_cols, axis=1)
    
    
    print("Mineral, Market and President DBs combined into:", money_df.columns)

    return money_df




