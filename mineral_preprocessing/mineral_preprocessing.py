""" This file loops throught the mineral data to generate a dataframe similar to the ETF dataframe that condenses the prices
of the given mineral by year."""

import pandas as pd
import time, os
from mineral_functions import (create_mineral_name, format_mineral, 
                            yearly_price, single_row_per_year, find_mineral_outliars)



# direction with mineral databases
dir_path = 'Data/mineral_data'


files = []

mineral_df = pd.DataFrame()

#counter objects
s_time = time.time()


for file in os.listdir(dir_path):
    file_pathway = dir_path +'/'+file
    files.append(file_pathway)
    
for file in files:
    # identify the assest being examined
    mineral = create_mineral_name(file)
    
    #adjust formatting
    formatted_df = format_mineral(file)
    
    #find first and last price per year
    start_end_price = yearly_price(formatted_df)
    
    # compile new dataframe with only 1 row per year
    single_row_df = single_row_per_year(start_end_price)
    
    complete_df = find_mineral_outliars(single_row_df)
    
    mineral_df = pd.concat([mineral_df, complete_df], ignore_index = True)
    
    print("Processed:", mineral)
    
    
end_time = time.time()        
print("Mineral Processing completed in:", end_time - s_time, "\n",
      "Mineral DataFrame Shape:", mineral_df.shape)
