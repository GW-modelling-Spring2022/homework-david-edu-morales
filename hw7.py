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

# define formula for solving K_unsat
def bcModel(Ks, b, theta):
    K_unsat = Ks*theta**(2*b+3)
    return K_unsat

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
soil_properties.set_index('texture', inplace=True)  # set soil names as index
soil_index = soil_properties.index.to_list()        # create a list of soil names

# %%
# create dataframe to recieve sat. calculations
matric_potentials = np.arange(-1000, 0, 0.1)
saturation = pd.DataFrame(matric_potentials, columns=['hm'])
saturation.set_index('hm',inplace=True)

for k in soil_index:
    # fix parameter values
    hb = soil_properties.loc[k].hb   # fix air entry pressure for soil
    b = soil_properties.loc[k].b     # fix pore size distribution for soil
    hm = saturation.index.to_list()     # create list of matric potential values
    saturation[k] = theta(hb, b, hm)

# %%
K_unsat = saturation.copy()         # make a copy of sat. df for K_unsat calculations

for k in soil_index:
    Ks = soil_properties.loc[k].Ks  # fix Ksat for soil
    b = soil_properties.loc[k].b    # fix pore size dist. for soil
    K_unsat[k] = K_unsat[k].apply(lambda x: bcModel(Ks, b, x))

# %%
saturation.index.to_list()
# %%
for k in soil_index:
    plt.plot(saturation[k],matric_potentials, label=k)
    plt.ylim(max(matric_potentials), min(matric_potentials))
    plt.legend()
plt.show()

plt.figure(figsize=(5,10))
for k in soil_index:

    plt.plot(saturation[k],K_unsat[k], label=k)
    plt.yscale('log')
    plt.legend()

# %%
water_content = saturation.copy()

for k in soil_index:
    n = soil_properties.loc[k].porosity
    water_content[k] =  water_content[k]*n
# %%
plt.figure(figsize=(5,8))
for k in soil_index:
    plt.plot(water_content[k],K_unsat[k], label=k)
    plt.yscale('log')
    plt.xlabel('Water content ('r'$\theta)$')
    plt.ylabel('Hydraulic conductivity [cm/s]')
    plt.title('Soil hydraulic conductivity function')
    plt.legend()
plt.show()

plt.figure(figsize=(5,8))
for k in soil_index:
    plt.plot(water_content[k],matric_potentials, label=k)
    plt.ylim(max(matric_potentials), min(matric_potentials))
    plt.xlabel('Water content ('r'$\theta)$')
    plt.ylabel('Matric head, h{} [cm]'.format('\N{LATIN SUBSCRIPT SMALL LETTER M}'))
    plt.legend()
    plt.title('Soil water characteristic curve')
plt.show()
# %%
