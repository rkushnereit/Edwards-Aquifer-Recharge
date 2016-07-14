import Basins
import pandas as pd


# Basins.SiteID('08192000',2015)
#
# discharge_data = 'Nueces_river_Uv_2015_discharge.csv'
#
# Basins.Rainfall_data(basin_csv=('Basin_1Lower.csv'),year=2015,ET_input=0)
#
# Basins.downstream_gage(discharge_data=discharge_data)
#
# Basins.BFI_solver(Separation_Method='IOH',k=.56150,C=0,gamma=0)
#
#
# #this is a test for git
#
#
# #this is a second line added to test git

Basins.master(USGS_site_ID='0819200',year=2015, basin_csv = 'Basin1Upper.csv', ET_input = 0, Separation_Method='IOH',k=.7531,C=0,gamma=0)
USGS_site_ID = '08192000'
year = 2015
df = pd.read_table('http://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=' + str(USGS_site_ID) + '&referred_module=sw&period=&begin_date=' + str(year) + '-01-01&end_date=' + str(year) + '-12-31',skiprows=26, index_col=2)
print(df.head())



