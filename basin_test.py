import Basins
import pandas as pd


#Basins.master(USGS_site_ID='08192000',year=2015, basin_csv = 'Basin_1Upper.csv', ET_input = 0, Separation_Method='L&H',k=.87517531,C=.249,gamma=00,Basin='Nueces')

#USGS 08169000 Comal Rv at New Braunfels, TX



df = pd.read_csv('Gauge_to_basin_table.csv')
df = df.set_index(df['Basin'])
print(df.head())


site_id = df.loc['Nueces']['Upper_Gauge1_ID']
site_id = str(site_id.replace('"',''))
print(site_id)

