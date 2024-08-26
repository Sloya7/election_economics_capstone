import pandas as pd 
import numpy as np
import os

#identifies the preprocessing for each database data source
database_preprocessors = [ 'president_preprocessing/president_preprocessing.py', 'mineral_preprocessing/mineral_preprocessing.py', 'ETF_preprocessing/ETF_preprocessing.py']

#runs the preprocessing 
for loc in database_preprocessors: 
    with open(loc) as file:
        exec(file.read())


#combines the markets and mineral dfs 
money_df = pd.concat([mineral_df, market_df], axis = 0, ignore_index= True)


# 6 news columns
# etf-up-count, etf-down-count, min-up-count,min-down-count
prior_years = []
election_years = president_df.ElectionYear.unique()
year1_list = []
year2_list = []

for y in president_df.ElectionYear.unique():
    prior_years.append(y-1)
    year1_list.append(y+1)
    year2_list.append(y+2)
    

#creates new columns to establish a relationship between election years and market data
money_df['ElectCycle'] = int
money_df['PriorYear'] = bool
money_df['ElectYear'] = bool
money_df['Year1'] = bool
money_df['Year2'] = bool

#assigns a boolan values for where in the election cycle a year is located
money_df['ElectYear'] = money_df['Year'].isin(election_years)
money_df['PriorYear'] = money_df['Year'].isin(prior_years)
money_df['Year1'] = money_df['Year'].isin(year1_list)
money_df['Year2'] = money_df['Year'].isin(year2_list)

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
    

        