from Create_ML.ML_config import *

def combine_data():

    #checks for preprocessed files and processed them if needed
    csv_names = {'markets': 'Cleaning_preprocessing/ETF_preprocessing/etf_preprocessing.py',
             'presidents': 'Cleaning_preprocessing/President_preprocessing/president_preprocessing.py', 
             'minerals': 'Cleaning_preprocessing/Mineral_preprocessing/mineral_preprocessing.py'}
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
     
     
     
    
    president_df = pd.read_csv('Cleaned_data/presidents')
    mineral_df = pd.read_csv('Cleaned_data/minerals')
    market_df = pd.read_csv('Cleaned_data/markets')
        
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
       

    #creates new columns to establish a relationship between election years and market data
    money_df['ElectCycle'] = int
    money_df['PriorYear'] = bool
    money_df['ElectYear'] = bool
    money_df['Year1'] = bool
    money_df['Year2'] = bool

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

    print("Mineral, Market and President DBs combined into:", money_df.columns)
    
    return money_df
