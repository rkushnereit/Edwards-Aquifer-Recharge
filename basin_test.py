import Basins
import pandas as pd
from ulmo.usgs import nwis
import numpy as np

Basins.master(Basin_name= 'Frio',year=2015, ET_input = 0, Separation_Method='IOH',k=.87517531,C=.249,gamma=00)

#USGS 08169000 Comal Rv at New Braunfels, TX

# Basin_name = 'Nueces'
#
# df = pd.read_csv('Gauge_to_basin_table.csv')
# df = df.set_index(df['Basin'])
# print(df.head())
#
#
# site_id = df.loc[Basin_name]['Upper_Gauge1_ID']
# site_id = str(site_id.replace('"',''))
# print(site_id)
#
