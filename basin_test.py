import Basins
import pandas as pd


Basins.SiteID('08192000',2015)

discharge_data = 'Nueces_river_Uv_2015_discharge.csv'

Basins.Rainfall_data(basin_csv=('Basin_1Lower.csv'),year=2015,ET_input=0)

Basins.downstream_gage(discharge_data=discharge_data)

Basins.BFI_solver(Separation_Method='IOH',k=.56150,C=0,gamma=0)


#this is a test for git


#this is a second line added to test git







