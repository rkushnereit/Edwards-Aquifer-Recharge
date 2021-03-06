import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import time
from ulmo.usgs import nwis
import numpy as np

start_time = time.time()
style.use(['fivethirtyeight','ggplot']) #,'dark_background'

def master(Basin_name = 'Nueces', year=2015, ET_input = 0, Separation_Method = 'IOH',k=.7531,C=.2469,gamma=0, basin_csv='#',USGS_site_ID = ('08192000')):
    basin_df = pd.read_csv('Gauge_to_basin_table.csv')
    basin_df = basin_df.set_index(basin_df['Basin'])


    site_id = basin_df.loc[Basin_name]['Lower_Gauge_ID']
    site_id = str(site_id.replace('"', ''))
    USGS_site_ID = str(site_id)
    print(USGS_site_ID)
    #discharge_data = pd.read_table(('http://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=' + str(USGS_site_ID) + '&referred_module=sw&period=&begin_date=' + str(year) + '-01-01&end_date=' + str(year) + '-12-31'), skiprows=25)
    #nwis.hdf5.update_site_data(USGS_site_ID)
    data = nwis.hdf5.get_site_data(USGS_site_ID, parameter_code='00060:00003')['00060:00003']
    discharge_data = pd.DataFrame(data['values']).drop(['last_checked', 'last_modified', 'qualifiers'], axis=1).set_index('datetime')
    discharge_data.value = discharge_data.value.apply(np.float)
    discharge_data.index = pd.to_datetime(discharge_data.index).to_period('D')

    discharge_data[discharge_data.values == -999999] = np.nan
    daily_groups = discharge_data.groupby((lambda d: d.month, lambda d: d.day))
    means = daily_groups.mean()

    start = str(str(year)+('0101'))
    end = str(str(year)+('1231'))

    discharge_data = discharge_data.ix[start:end].copy()
    discharge_data['Discharge'] = discharge_data['value']
    del discharge_data['value'] #.copy()
    # discharge_data.reset_index(drop = True,inplace = True)
    # print(discharge_data.head(10))
    # discharge_data = discharge_data[discharge_data['agency_cd'] != '5s']
    # #discharge_data = discharge_data.drop([0])
    # #C = 1-k
    # discharge_data.reset_index(drop = True,inplace = True)
    # print(discharge_data.head())
    # print(discharge_data.tail())

    basin_csv = basin_df.loc[Basin_name]['Lower_Basin_ID']
    basin_csv = str(basin_csv.replace('"', '') + '.csv')
    # print(basin_csv)
    Weighted_basin_csv = pd.read_csv(basin_csv)
    # print(Weighted_basin_csv.head())
    basin_csv = pd.read_csv(basin_csv)
    for i in range(0, len(Weighted_basin_csv['Jan-15']) - 1):
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
    print('The square footage of this basin is ' + str(sum_Area_basin_csv) + ' ft^2 or ' + str(sum_Area_basin_csv*(2.26598**(-5))) + ' acres or ' + str(sum_Area_basin_csv*(3.587**(-8))))
    print('The Precipitation for the year '+str(year) +' is ' + str(yearly_total_basin_csv) + ' inches.')

    # discharge_df = pd.DataFrame()
    # discharge_df = discharge_df.reset_index(drop=True)
    # print(discharge_df.head())
    discharge_df = discharge_data
    discharge_df.reset_index(drop = False, inplace = True)
    #discharge_df['Discharge'] = discharge_data[['value']].astype(float)
    #discharge_df = discharge_df.set_index(pd.DatetimeIndex(discharge_df['datetime']))
    discharge_df['baseflow'] = 0.0


    if Separation_Method == 'IOH':
        for i in range(0, len(discharge_df['Discharge'])-1):
            if (discharge_df.iloc[i]['Discharge'] * k <= (discharge_df.iloc[i - 1]['Discharge'])) & (discharge_df.iloc[i]['Discharge'] * k <= discharge_df.iloc[i + 1]['Discharge']):
                discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']
            else:
                discharge_df.ix[i,['baseflow']] = None

    # if Separation_Method == 'IOH_Modified':
    #     for i in range(0, len(discharge_df['Discharge'])-1):
    #         if (discharge_df.iloc[i]['Discharge'] * k <= discharge_df.iloc[i - 1]['Discharge']) & (discharge_df.iloc[i]['Discharge'] * k <= discharge_df.iloc[i + 1]['Discharge']):
    #             discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']
    #         else:
    #             discharge_df.ix[i,['baseflow']] = None
    #     for i in range(0, len(discharge_df['Discharge'])-1):
    #         if (discharge_df.loc[i]['Discharge'] * (k**i) <= discharge_df.iloc[i - 1]['Discharge']) & (discharge_df.iloc[i]['Discharge'] * k <= discharge_df.iloc[i + 1]['Discharge']):

    elif Separation_Method == 'Chapman':
        for i in range(0, len(discharge_df['Discharge'])-1):
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
        for i in range(0, len(discharge_df['Discharge'])-1):
            if ((k / (1 + C)) * discharge_df.iloc[i - 1]['Discharge']) + (C / (1 + C) * (
                discharge_df.iloc[i]['Discharge'] + gamma * discharge_df.iloc[i - 1]['Discharge'])) >= \
                    discharge_df.iloc[i]['Discharge']:
                discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']
            else:
                discharge_df.ix[i,['baseflow']] = None

    elif Separation_Method == 'L&H':
        for i in range(0, len(discharge_df['Discharge'])-1):
            discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']
            if (gamma * discharge_df.iloc[i - 1]['Discharge']) + (discharge_df.iloc[i]['Discharge'] - discharge_df.iloc[i - 1]['Discharge']) * ((1 + gamma) / 2) <= 0.0:
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
        if ((discharge_df.iloc[i]['baseflow']) > float(discharge_df.iloc[i]['Discharge'])):
            discharge_df.ix[i,['baseflow']] = discharge_df.iloc[i]['Discharge']


    del discharge_df['datetime']
    BFI = (discharge_df['baseflow'].sum())/discharge_df['Discharge'].sum()
    if BFI >= .61:
        BFI = (discharge_df['baseflow'].sum())/(discharge_df['baseflow'].sum() + discharge_df['Discharge'].sum())
    print('BFI = ' + str(BFI))
    recharge = (BFI * ((Precip - ET_input)/12) * area)
    recharge = recharge * (2.29568*(10**(-5))) # convert to acre-ft
    print('The estimated recharge using the ' + str(Separation_Method) + ' method, and a k value of ' + str(k) + ' is ' , recharge , ' acre-ft')
    discharge_df['Fld_Flw'] = None
    print("--- %s seconds ---" % (time.time() - start_time))
    ax = discharge_df.plot(title= basin_df.loc[Basin_name]['Lower_Gauge_name'] + ', k = ' + str(k), figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel('datetime', fontsize=12)
    ax.set_ylabel('discharge_cfs', fontsize=12)
    plt.show()

# Rainfall_data(pd.read_csv('Basin_1Upper.csv'),2015,0)
# discharge_data = 'Nueces_river_Uv_2015_discharge.csv'
# downstream_gage(discharge_data)
# # 'IOH' , 'Chapman' , 'Boughton' , 'IHACRES' , 'L&H'
# BFI_solver('IOH',.5678,0,0)










