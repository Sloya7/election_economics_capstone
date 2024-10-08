
""" This applies the work found in the ETF_preprocessing_development.ipynb into usable functions as a py file """

from Cleaning_preprocessing.config import *

### Takes file_path and returns the last part of it without the extension

def create_etf_name(file_path):
    etf_name = os.path.basename(os.path.normpath(file_path))
    etf_name = etf_name.replace('.txt', '')
    return etf_name


### Creates inital DF and removes columns, adds new ones
def format_checking(file_path):
    #read file
    try:
        etf_df = pd.read_csv(file_path, encoding='utf-8')
        drop_columns =  ["OpenInt", "Volume", "Low", "High"]
        for c in drop_columns:
            if c in etf_df.columns:
                return etf_df
        else:
            return 1
        
    except pd.errors.ParserError as e:
        print(f"Parsing error: {e} in file:", create_etf_name(file_path), )
        return 1
    except Exception as e: 
        print("Formmating error in file:", create_etf_name(file_path), )
        return 1

def format_columns(checked_path, etf_name):
    #drop columns
    drop_columns =  ["OpenInt", "Volume", "Low", "High"]
    
    
    checked_path.drop(drop_columns, axis = 1, inplace = True)
    
    #add value changed column
    checked_path['change']= checked_path['Close'] - checked_path['Open']
    #add the etf's name
    checked_path['ETF_name'] = etf_name
    
    return checked_path
 
### Coverts date from string to datetime format 
# and creates new column with year only 

def format_dates(formatted_df):
    if type(formatted_df) == int: 
        return 1
    formatted_date = pd.DataFrame(formatted_df)
    formatted_date['Date'] = pd.to_datetime(formatted_date['Date']) 
    formatted_date['Year'] = formatted_date.Date.dt.year
    return formatted_date



### Creates outliar limits grouped by year

def find_yearly_limits(df):
    # create dataframe grouped by year
    year_df = df.groupby('Year')
    
    # Find the first and last day of the year for each year
    earliest_dates = year_df.Date.min()
    last_dates = year_df.Date.max()
    
    start_end_dates = df.query(
        "Date in @earliest_dates or Date in @last_dates")
    
    year = start_end_dates.Year.unique()
    
    # create dataframe that to place needed values in
    output_df = pd.DataFrame(columns = [ 'Year','Asset_name','Year_Open', 'Year_Close', 'Year_Change', 'Loss', 'Gain'])


    #loop to generate new row in output database
    for i in start_end_dates.Year.unique():

        #groups date data by year
        year_df = start_end_dates[start_end_dates.Year == i]

        #uses objects to reference needed values
        try: 
            open = year_df.iloc[0].Open
            close = year_df.iloc[1].Close
            change = close - open
            
            # creates mapping array 
            new_row = {'Year':i, 'Asset_name':year_df.iloc[0].ETF_name, 'Year_Open':open, 'Year_Close':close, 'Year_Change':change}
            
            # inserts data into new row of the output dataframe
            output_df.loc[len(output_df)] = new_row
        except Exception as e:
            print("Missing Date Values in file:", year_df.iloc[0].ETF_name)
            return 1

    #fill NaNs with a default string value
    output_df['Loss'] = 'no'
    output_df['Gain'] = 'no'
    
    return output_df


### Finds the outliar years and changes the string value to 'yes'

def find_outliars(df):
    # sets the 80% and 20% boundries
    etf_high_lim = df.Year_Change.quantile(.8)
    etf_low_lim = df.Year_Change.quantile(.2)
    
    # compare the mean value of each year to the 20 and 80 limits previously set and 
    # create a column documenting if it was outside the low/high lim

    for i in range(len(df)):
        if df.Year_Change.iloc[i] < etf_low_lim:
            df.loc[i, 'Loss'] = 'yes'
        elif df.Year_Change.iloc[i] > etf_high_lim:
            df.loc[i,'Gain'] = 'yes'
        else: 
            continue
    
    return df
    
    

    
    