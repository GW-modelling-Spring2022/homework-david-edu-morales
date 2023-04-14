# %%
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# %%
# define formula for solving saturation
def theta(hb,b,hm):
    for i in hm:
        if i < hb:
            theta = (hm/hb)**(-1/b)
            print('ok')
        else:
            theta = 1
    return theta

def theta2(hb,b,hm):
    soil_sat_index = range(len(hm))
    soil_sat = []
    for i in soil_sat_index:
        if hm[i] < hb:
            theta = (hm/hb)**(-1/b)
            soil_sat[i] = theta
        else:
            soil_sat[i] = 1
    return soil_sat

def theta3(hb, b, hm):
    hm_length = len(hm)
    soil_sat_index = np.arange(0, hm_length, 1)
    soil_sat = np.zeros(hm_length)

    for i in soil_sat_index:
        if hm[i] < hb:
            theta = (hm[i]/hb)**(-1/b)
            soil_sat[i] = theta
        else:
            soil_sat[i] = 1
    return soil_sat

d = {'texture': ['sand','loamy sand','sandy loam','silt loam','loam','clay loam','sandy clay','silty clay','clay'],
         'porosity' : [.395,.41,.435,.485,.451,.476,.426,.492,.482],
         'Ks' : [1.76e-2,1.56e-2,3.47e-3,7.2e-4,6.95e-4,2.45e-4,2.17e-4,1.03e-4,1.28e-4],
         'hb' : [-12.1,-9,-21.8,-78.6,-47.8,-63,-15.3,-49,-40.5],
         'b'  : [4.05,4.38,4.9,5.3,5.39,8.52,10.4,10.4,11.4],
         'hm' : [4.95,6.13,11.01,16.68,8.89,20.88,23.9,29.22,31.63]
        }

# create dataframe of soil characteristics
soil_properties = pd.DataFrame(d)
# create a list of soil names
soilList = soil_properties.texture.to_list()
# set soil names as index
soil_properties.set_index('texture', inplace=True)

# %%
saturation = pd.DataFrame(np.arange(-1000,0,0.01), columns=['hm'])
saturation.set_index('hm',inplace=True)
hm = saturation.index.to_list()
# %%
for soil in soil_properties.index.to_list():
    hb = soil_properties.loc[soil].hb
    b = soil_properties.loc[soil].b
    hm = saturation.index.to_list()
    saturation[soil] = theta3(hb, b, hm)
# %%
soil_sat_index = np.arange(0,10,1)
soil_sat = np.zeros(len(soil_sat_index))
hb = -12.1
b = 4.05

for i in soil_sat_index:
    if hm[i] < hb:
        theta = (hm[i]/hb)**(-1/b)
        soil_sat[i] = theta
    else:
        soil_sat[i] = 1