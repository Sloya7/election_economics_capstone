""" This file plots the distribution of data feed into the ML """

from Model_inspections.__init__ import *
from saved_ML_models import *
import matplotlib.pyplot as plt





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
            
    
""" Display the distribution of avaliable data from the Market Data Source"""  
    
#file locations
president_df = pd.read_csv('Cleaned_data/presidents.csv')
mineral_df = pd.read_csv('Cleaned_data/minerals.csv')
market_df = pd.read_csv('Cleaned_data/markets.csv')

data_dfs = [mineral_df,market_df]

# shows the amount of data available for each year
year_count = market_df.Year
plt.hist(year_count, color='green')

# make x ticks print years in whole numbers
loc, labels = plt.xticks()
print((year_count.min()), (year_count.max()))
plt.xticks(np.arange(year_count.min(), year_count.max(),1), rotation = 60)

#add title and display plot
plt.title('Number of ETFs analyzed per Year')
plt.show()




""" Display the precent of gains in gold data"""

x_values = mineral_df[mineral_df.Asset_name == 'gold_price'].Gain.value_counts()
plt.pie(x_values, labels = x_values.index)
plt.legend(x_values,
            loc="center left",
            bbox_to_anchor=(.9, 0, 0.75, 1),
            title = 'Yearly Gain over 80%?')

plt.title('Gold Gains')
plt.show()