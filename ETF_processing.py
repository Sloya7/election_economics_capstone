from preprocessing_functions import (create_etf_name, format_checking, format_columns, 
    format_dates, find_yearly_limits, find_outliars)
import os, time
import pandas as pd


# DataFrame to be populated

market_df = pd.DataFrame()

# ID the directory housing the market data
dir_path = 'Data/markets_test'
#List to house file path strings
files = []

#Create and append file names into the files list
for file in os.listdir(dir_path):
    file_pathway = dir_path +'/'+file
    files.append(file_pathway)


#counter objects
f_count = 0
s_time = time.time()

#list of files not properly processed
error_files = []

#loops to process the market files
for file in files:

    etf_named = create_etf_name(file)
    
    # if file name had errors    
    if etf_named == 1:
        error_files.append(file)
        continue
    
    else: 
        formatted_df = format_checking(file)
        if not isinstance(formatted_df, pd.DataFrame):
            error_files.append(file)
            continue
        
        columned_df = format_columns(formatted_df, etf_named)

        dated_df = format_dates(columned_df)
        
        if type(dated_df) == int:
            error_files.append(file)
            continue

        limits_df = find_yearly_limits(dated_df)
        if not isinstance(limits_df, pd.DataFrame):
            error_files.append(file)
            continue

        completed_df = find_outliars(limits_df)
        
        market_df = pd.concat([market_df, completed_df], ignore_index= True)
        
        f_count += 1
        cur_time = time.time()
        if f_count % 250 == 0: 
            print('file {} complete'.format(f_count))
            print('Time Elapsed: ', cur_time - s_time)
            
end_time = time.time()        
print("Market Processing completed in:", end_time - s_time, "\n",
      "Market DataFrame Shape:", market_df.shape, "\n",
      "No. of Files removed due to errors:", len(error_files))

