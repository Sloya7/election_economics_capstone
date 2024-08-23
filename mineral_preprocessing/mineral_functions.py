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
    
    #adjust dtypes
    formatted_df.date = pd.to_datetime(formatted_df.date)
    
    #add columns specifing year
    formatted_df['Year'] = formatted_df.date.dt.year
    mineral_name = create_mineral_name(file)
    formatted_df['Asset'] = mineral_name
    
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
    output_df = pd.DataFrame(columns = [ 'Year', 'Asset_name', 'Year_Open', 'Year_Close', 'Year_Change', 'Loss', 'Gain'])

    #loop to generate new row in output database
    for i in start_end_dates.Year.unique():
        
        #groups date data by year
        year_df = start_end_dates[start_end_dates.Year == i]

        #uses objects to reference needed values
        open = year_df.iloc[0].price
        close = year_df.iloc[1].price
        change = close - open
        
        # creates mapping array 
        new_row = {'Year':i, 'Asset_name': year_df.loc[0,'Asset'], 'Year_Open':open, 'Year_Close':close, 'Year_Change':change}
        
        # inserts data into new row of the output dataframe
        output_df.loc[len(output_df)] = new_row

    output_df['Loss'] = 'no'
    output_df['Gain'] = 'no'

    return output_df
    
### The find_outliars function from ETF preprocessing can be used on this last step as well ###