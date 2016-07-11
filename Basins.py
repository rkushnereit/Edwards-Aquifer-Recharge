import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use(['fivethirtyeight','ggplot']) #,'dark_background'
#
# def Basin(River_Basin, BFI_Filter, year, Rainfall, DS_gage,Up_gage1):
#      fgh =0
     
def Rainfall_data(basin_csv,year, ET_input = 0):
    global ET
    global Precip
    global area
    ET = ET_input

    Weighted_basin_csv = basin_csv
    for i in range(0, Weighted_basin_csv['Jan-15'].shape[0] - 1):
        Weighted_basin_csv.ix[i,['Jan-15']] = basin_csv.iloc[i]['Jan-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Feb-15']] = basin_csv.iloc[i]['Feb-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Mar-15']] = basin_csv.iloc[i]['Mar-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Apr-15']] = basin_csv.iloc[i]['Apr-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['May-15']] = basin_csv.iloc[i]['May-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Jun-15']] = basin_csv.iloc[i]['Jun-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Jul-15']] = basin_csv.iloc[i]['Jul-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Aug-15']] = basin_csv.iloc[i]['Aug-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Sep-15']] = basin_csv.iloc[i]['Sep-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Oct-15']] = basin_csv.iloc[i]['Oct-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Nov-15']] = basin_csv.iloc[i]['Nov-15'] * basin_csv.iloc[i]['Shape_Area']
        Weighted_basin_csv.ix[i,['Dec-15']] = basin_csv.iloc[i]['Dec-15'] * basin_csv.iloc[i]['Shape_Area']

    sum_Area_basin_csv = Weighted_basin_csv['Shape_Area'].sum()
    sum_Jan = Weighted_basin_csv['Jan-15'].sum() / sum_Area_basin_csv
    sum_Feb = Weighted_basin_csv['Feb-15'].sum() / sum_Area_basin_csv
    sum_Mar = Weighted_basin_csv['Mar-15'].sum() / sum_Area_basin_csv
    sum_Apr = Weighted_basin_csv['Apr-15'].sum() / sum_Area_basin_csv
    sum_May = Weighted_basin_csv['May-15'].sum() / sum_Area_basin_csv
    sum_Jun = Weighted_basin_csv['Jun-15'].sum() / sum_Area_basin_csv
    sum_Jul = Weighted_basin_csv['Jul-15'].sum() / sum_Area_basin_csv
    sum_Aug = Weighted_basin_csv['Aug-15'].sum() / sum_Area_basin_csv
    sum_Sep = Weighted_basin_csv['Sep-15'].sum() / sum_Area_basin_csv
    sum_Oct = Weighted_basin_csv['Oct-15'].sum() / sum_Area_basin_csv
    sum_Nov = Weighted_basin_csv['Nov-15'].sum() / sum_Area_basin_csv
    sum_Dec = Weighted_basin_csv['Dec-15'].sum() / sum_Area_basin_csv

    Monthly_list = {'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    'monthly_weighted_average': [sum_Jan, sum_Feb, sum_Mar, sum_Apr, sum_May, sum_Jun, sum_Jul, sum_Aug,
                                                 sum_Sep, sum_Oct, sum_Nov, sum_Dec]}
    Monthly = pd.DataFrame(Monthly_list)
    yearly_total_basin_csv = Monthly['monthly_weighted_average'].sum()
    area = sum_Area_basin_csv
    Precip = yearly_total_basin_csv
    print('The square footage of this basin is ' + str(sum_Area_basin_csv) + ' ft^2')
    print('The Precipitation for the year '+str(year) +' is ' +str(yearly_total_basin_csv) + ' inches.')

def downstream_gage(discharge_data):
    global station_name
    station_name = discharge_data
    discharge_data = pd.read_csv(discharge_data)
    global discharge_df
    discharge_df = pd.DataFrame()
    discharge_df = discharge_df.reset_index(drop=True)
    discharge_df['Date'] = discharge_data[[0]]
    discharge_df['Discharge'] = discharge_data[[1]]
    discharge_df = discharge_df.set_index(pd.DatetimeIndex(discharge_df['Date']))


def BFI_solver(Separation_Method,k=.7531,C=0,gamma=0):

    discharge_df['baseflow'] = 0#discharge_df[[1]]

    if Separation_Method == 'IOH':
        for i in range(0, len(discharge_df['Discharge'])-1):
            if (discharge_df.iloc[i]['Discharge'] * k <= discharge_df.iloc[i - 1]['Discharge']) & (discharge_df.iloc[i]['Discharge'] * k <= discharge_df.iloc[i + 1]['Discharge']):
                discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']
            else:
                discharge_df.ix[i,['baseflow']] = None

    elif Separation_Method == 'Chapman':
        for i in range(0, len(discharge_df['Discharge'])):
            if (((k / (2 - k)) * discharge_df.iloc[i - 1]['Discharge']) + ((1 - k) / (2 - k) * discharge_df.iloc[i]['Discharge'])) >= discharge_df.iloc[i]['Discharge']:
                discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']
            else:
                discharge_df.ix[i,['baseflow']] = None

    elif Separation_Method == 'Boughton':
        for i in range(0, (discharge_df['Discharge'].shape[0] - 1)):
            if ((k / (1 + C)) * discharge_df.iloc[i - 1]['Discharge']) + (
                    C / (1 + C) * discharge_df.iloc[i]['Discharge']) >= discharge_df.iloc[i]['Discharge']:
                discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']
            else:
                discharge_df.ix[i,['baseflow']] = None

    elif Separation_Method == 'IHACRES':
        for i in range(0, len(discharge_df['Discharge'])):
            if ((k / (1 + C)) * discharge_df.iloc[i - 1]['Discharge']) + (C / (1 + C) * (
                discharge_df.iloc[i]['Discharge'] + gamma * discharge_df.iloc[i - 1]['Discharge'])) >= \
                    discharge_df.iloc[i]['Discharge']:
                discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']
            else:
                discharge_df.ix[i,['baseflow']] = None

    elif Separation_Method == 'L&H':
        for i in range(0, len(discharge_df['Discharge'])):
            discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']
            if (gamma * discharge_df.iloc[i - 1]['Discharge']) + (
                discharge_df.iloc[i]['Discharge'] - discharge_df.iloc[i - 1]['Discharge']) * ((1 + gamma) / 2) <= 0:
                discharge_df['baseflow'] = discharge_df.iloc[i]['Discharge']
            else:
                discharge_df['baseflow'] = None
    else:
        print('Invalid separation method, please enter a proper filter.')
        print('IOH , Chapman , Boughton , IHACRES , L&H')

    discharge_df.ix[1, ['baseflow']] = discharge_df.iloc[1]['Discharge']
    discharge_df.ix[int(len(discharge_df))-1, ['baseflow']] = discharge_df.iloc[int(len(discharge_df))-1]['Discharge']
    discharge_df['baseflow'] = discharge_df['baseflow'].interpolate(method='linear')
    for i in range(0, len(discharge_df['Discharge'])):
        if (discharge_df.iloc[i]['baseflow'] > discharge_df.iloc[i]['Discharge']):
            discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']


    del discharge_df['Date']
    BFI = (discharge_df['baseflow'].sum())/(discharge_df['baseflow'].sum() +discharge_df['Discharge'].sum())
    recharge = (BFI * ((Precip - ET)/12) * area) *(2.29568*(10**(-5)))
    print('The estimated recharge using the ' + str(Separation_Method) + ' method, and a k value of ' + str(k) + ' is ' , recharge , ' acre-ft')
    discharge_df['Fld_Flw'] = None
    #discharge_df['Specific_conductance'] = df['Specific_conductance']
    ax = discharge_df.plot(title= station_name + ', k = ' + str(k), figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('discharge_cfs', fontsize=12)
    plt.show()

# Rainfall_data(pd.read_csv('Basin_1Upper.csv'),2015,0)
# discharge_data = 'Nueces_river_Uv_2015_discharge.csv'
# downstream_gage(discharge_data)
# # 'IOH' , 'Chapman' , 'Boughton' , 'IHACRES' , 'L&H'
# BFI_solver('IOH',.5678,0,0)










