import pandas as pd 
import os



def create_mineral_name(file_path):
    mineral_name = os.path.basename(os.path.normpath(file_path))
    mineral_name = mineral_name.replace('.csv', '')
    return mineral_name
    

# import and correct dtypes of date and create a Year column for grouping
def format_mineral(file):
    #import/read csv
    mineral_df = pd.read_csv(file)
    
    #drop na rows
    formatted_df = mineral_df.dropna()
    formatted_df = formatted_df.copy()
    
    #adjust dtypes
    formatted_df.date = pd.to_datetime(formatted_df.date)
    
    #add columns specifing year
    formatted_df['Year'] = formatted_df.date.dt.year
    
    # add columns with assest description 
    formatted_df['Asset'] = create_mineral_name(file)
    
    return formatted_df

# create df that take only the earliest and last day of each year
def yearly_price(formatted_df):
    #group by year
    yearly_gold = formatted_df.groupby(formatted_df.Year)
    
    # Find the first and last day of the year for each year
    earliest_dates = yearly_gold.min()
    last_dates = yearly_gold.max()
    start_end_dates = formatted_df.query("date in @earliest_dates.date or date in @last_dates.date")
    return start_end_dates

def single_row_per_year(start_end_dates):
    output_df = pd.DataFrame(columns = ['Year', 'Asset_name', 'Year_Open', 'Year_Close', 'Year_Change', 'Loss', 'Gain'])

    #loop to generate new row in output database
    for i in start_end_dates.Year.unique():
        
        #groups date data by year
        year_df = start_end_dates[start_end_dates.Year == i]

        #uses objects to reference needed values     
        open = year_df.iloc[0].price
        close = year_df.iloc[1].price
        change = close - open

        # creates mapping array 
        new_row = {'Year':i, 'Asset_name':year_df.Asset.iloc[0], 'Year_Open':open, 'Year_Close':close, 'Year_Change':change}

        # inserts data into new row of the output dataframe
        output_df.loc[len(output_df)] = new_row

    output_df['Loss'] = 'no'
    output_df['Gain'] = 'no'

    return output_df
    
def find_mineral_outliars(df):
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