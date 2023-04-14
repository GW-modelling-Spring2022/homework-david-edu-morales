# %%
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# %%
# define formula for solving saturation
def theta(hb, b, hm):
    hm_length = len(hm)                 # count elements in matric potential list
    index = np.arange(0, hm_length, 1)  # set an index from zero to N of hm
    soil_sat = np.zeros(hm_length)      # create an array as long as index

    for i in index:
        if hm[i] < hb:                  # calculate sat. for hm < air entry pressure
            theta = (hm[i]/hb)**(-1/b)
            soil_sat[i] = theta
        else:                           # set sat. to 1 for values >= air entry pressure
            soil_sat[i] = 1
    return soil_sat

# create dictionary of soil properties
d = {'texture': ['sand','loamy sand','sandy loam','silt loam','loam','clay loam','sandy clay','silty clay','clay'],
         'porosity' : [.395,.41,.435,.485,.451,.476,.426,.492,.482],
         'Ks' : [1.76e-2,1.56e-2,3.47e-3,7.2e-4,6.95e-4,2.45e-4,2.17e-4,1.03e-4,1.28e-4],
         'hb' : [-12.1,-9,-21.8,-78.6,-47.8,-63,-15.3,-49,-40.5],
         'b'  : [4.05,4.38,4.9,5.3,5.39,8.52,10.4,10.4,11.4],
         'hm' : [4.95,6.13,11.01,16.68,8.89,20.88,23.9,29.22,31.63]
        }

# create dataframe of soil characteristics
soil_properties = pd.DataFrame(d)
soilList = soil_properties.texture.to_list()        # create a list of soil names
soil_properties.set_index('texture', inplace=True)  # set soil names as index

# %%
# create dataframe to recieve sat. calculations
saturation = pd.DataFrame(np.arange(-1000,0,0.01), columns=['hm'])
saturation.set_index('hm',inplace=True)

soil_index = soil_properties.index.to_list()

for soil in soil_index:
    # fix parameter values
    hb = soil_properties.loc[soil].hb   # fix air entry pressure for soil
    b = soil_properties.loc[soil].b     # fix pore size distribution for soil
    hm = saturation.index.to_list()     # create list of matric potential values
    saturation[soil] = theta(hb, b, hm)

# %%
def bcModel(Ks, b, theta):
    K_unsat = Ks*theta**(2*b+3)
    return K_unsat