from preprocessing_functions import (create_etf_name, format_columns, 
    format_dates, find_yearly_limits, find_outliars)

etf_files = ['Data/markets_test/aaxj.us.txt', 'Data/markets_test/aadr.us.txt']

# ID file location
for file in etf_files:
    
    file_path = file

    etf_named = create_etf_name(file_path)

    formatted_df = format_columns(file_path, etf_named)

    dated_df = format_dates(formatted_df)

    limits_df = find_yearly_limits(dated_df)

    completed_df = find_outliars(limits_df)


    print(completed_df.iloc[1])

