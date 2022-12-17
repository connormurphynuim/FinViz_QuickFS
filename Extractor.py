import pandas as pd
import numpy as np

#Create raw data dataframe
base_df = pd.read_csv('FinvizExtract.csv')

#Create copy of dataframe to work on
df = base_df.copy()

#Create country exclusions list
Country_Exclusions = ['China', 'Hong Kong', 'Russia']

#Remove countries
df = df[df['Country'].isin(Country_Exclusions) == False]

#Create bins to smoothout data
PE_Threshold = [i for i in np.arange(0, 35, 0.25).round(2)]
DEq_Threshold = [i for i in np.arange(0, 3, 0.15).round(2)]
CQ_Ratio = [i for i in np.arange(0, 3, 0.10).round(2)]

#Function to appy bins to column data
def bin_setter(x,thres_list):
    for i, value in enumerate(thres_list):
        if x > max(thres_list) or x == max(thres_list):
            y = max(thres_list)
            break
        elif thres_list[i] <= x and x < thres_list[i+1]:
            y = thres_list[i+1]
            break

    return y


#Applying bins to data
df['P/E'] = df['P/E'].apply(bin_setter, thres_list=PE_Threshold)
df['Debt/Eq'] = df['Debt/Eq'].apply(bin_setter, thres_list=DEq_Threshold)
df['LT Debt/Eq'] = df['LT Debt/Eq'].apply(bin_setter, thres_list=DEq_Threshold)
df['Current Ratio'] = df['Current Ratio'].apply(bin_setter, thres_list=CQ_Ratio)
df['Quick Ratio'] = df['Quick Ratio'].apply(bin_setter, thres_list=CQ_Ratio)


#Create sub dataframe with only the columns of interest which will be used to rank
rank_df = df[['Company Name', 'Ticker', 'Sector', 'Industry', 'Country',
       'P/E','Debt/Eq', 'LT Debt/Eq', 'P/FCF', 'Current Ratio', 'Quick Ratio', 'P/C', 'Price', 'Dividend %'
       , 'Dividend', 'Profit Margin']]

#Create list of columns the data is to be partitioned on and sorted on
partiton_cols = ['Sector', 'Industry']
sort_cols = ['Sector', 'Industry','P/E','Debt/Eq', 'LT Debt/Eq', 'P/FCF', 'Current Ratio', 'Quick Ratio']

#Create ranks for data
rank_df['Rank'] = rank_df.sort_values(sort_cols,ascending=True).groupby(partiton_cols).cumcount()+1

#Sort the data and filter using the query method
rank_sort_df = rank_df.sort_values(by=sort_cols)#.query('Rank<=3')

#print to screen
print(rank_sort_df.to_string())