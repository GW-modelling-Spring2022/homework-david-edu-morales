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

# define formula for solving infiltration duration (seconds)
def infil_duration(wc_initial, Ft, df):
    Ft_length = len(Ft)                 # count elements in matric potential list
    index = np.arange(0, Ft_length, 1)  # set an index from zero to N of hm
    times = np.zeros(Ft_length)      # create an array as long as index

    K = df.Ks
    hm = abs(df.hm)
    n = df.porosity
    capacity = n-wc_initial

    for i in index:

        t = (1/K)*(Ft[i]-hm*capacity*np.log(1+(Ft[i]/(hm*capacity))))
        times[i] = t
    return times

def infiltration_capacity(wc_initial, Ft, df):
    Ft_length = len(Ft)                 # count elements in matric potential list
    index = np.arange(0, Ft_length, 1)  # set an index from zero to N of hm
    infil_rate = np.zeros(Ft_length)      # create an array as long as index

    K = df.Ks
    hm = df.hm
    n = df.porosity
    capacity = n-wc_initial

    for i in index:
        f_c = K*((abs(hm)*(capacity)/Ft[i])+1)
        infil_rate[i] = f_c
    return infil_rate

# Numerically integrate the water content for ea. soil w/ water table 1m below surface
def water_content(hb, b, n):
    hb = hb*-1
    u = hb
    v = 100               # depth from surface to top of capillary fringe
    B = b-1
    water_content = -n*(hb**(1/b))*(b/(b-1))*(u**(B/b)-v**(B/b))
    return water_content

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


# %%
soil_prop_1m = soil_properties.copy()

soil_prop_1m['water_content'] = soil_prop_1m.apply(lambda x: water_content(x.hb, x.b, x.porosity),
                                                   axis=1)
soil_prop_1m['depth'] = soil_prop_1m.apply(lambda x: 100+x.hb, axis=1)
soil_prop_1m['storage_capacity'] = soil_prop_1m.apply(lambda x: x.depth*x.porosity-x.water_content, axis=1)

# %%
infiltration = np.arange(.05, 10, 0.05)
sand_infil_capacity = pd.DataFrame(infiltration, columns=['F']); sand_time_to_infil = pd.DataFrame(infiltration, columns=['F'])
sand_infil_capacity.set_index('F', inplace=True); sand_time_to_infil.set_index('F', inplace=True)

sand_wc = [0, 0.1, 0.2, 0.3, 0.394]

for k in sand_wc:
    Ft = sand_infil_capacity.index.to_list()
    sand_infil_capacity[str(k)] = infiltration_capacity(k, Ft, soil_properties.loc[['sand']])
    sand_time_to_infil[str(k)] = infil_duration(k, Ft, soil_properties.loc[['sand']])    

plt.figure(figsize=(8,5))
for k in sand_wc:
    plt.plot(sand_time_to_infil[str(k)], sand_infil_capacity[str(k)], label='initial soil moisture, '+str(k))
    plt.xlabel('Time (seconds)')
    plt.ylabel('Infiltration capacity, fc(t) [cm/s]')
    plt.legend()
    plt.semilogx()
    plt.ylim(0,.2)
    plt.title('Infiltration capacity for Sand')

# %%
infiltration = np.arange(.05, 3, 0.05)
cumulative_infil = pd.DataFrame(infiltration, columns=['F'])
cumulative_infil.set_index('F', inplace=True)

sand_wc = [0, 0.1, 0.2, 0.3, 0.394]

def infiltration_capacity(wc_initial, Ft, df):
    Ft_length = len(Ft)                 # count elements in matric potential list
    index = np.arange(0, Ft_length, 1)  # set an index from zero to N of hm
    infil = np.zeros(Ft_length)      # create an array as long as index

    K = df.Ks
    hm = abs(df.hm)
    n = df.porosity
    capacity = n-wc_initial

    for i in index:

        t = (1/K)*(Ft[i]-hm*capacity*np.log(1+(Ft[i]/(hm*capacity))))
        infil[i] = t
    return infil

for k in sand_wc:
    Ft = cumulative_infil.index.to_list()
    cumulative_infil[str(k)] = infiltration_capacity(k, Ft, soil_properties.loc[['sand']])

plt.figure(figsize=(8,5))
for k in sand_wc:
    plt.plot(cumulative_infil[str(k)], cumulative_infil.index.to_list(), label='initial soil moisture, '+str(k))
    plt.xlabel('Time (seconds)')
    plt.ylabel('Cumulative infiltration, F(t) [cm]')
    plt.legend()
    plt.title('Cumulative infiltration for Sand')

plt.show()

# %%
infiltration = np.arange(.05, 3, 0.05)
cumulative_infil = pd.DataFrame(infiltration, columns=['F'])
cumulative_infil.set_index('F', inplace=True)

clay_wc = [0, 0.1, 0.2, 0.3, 0.4, .482]

for k in clay_wc:
    Ft = cumulative_infil.index.to_list()
    cumulative_infil[str(k)] = infiltration_capacity(k, Ft, soil_properties.loc[['clay']])

plt.figure(figsize=(8,5))
for k in clay_wc:
    plt.plot(cumulative_infil[str(k)], cumulative_infil.index.to_list(), label='initial soil moisture, '+str(k))
    plt.xlabel('Time (seconds)')
    plt.ylabel('Cumulative infiltration, F(t) [cm]')
    plt.legend()
    plt.title('Cumulative infiltration for Clay')

plt.show()

# %%
infiltration = np.arange(.05, 10, 0.05)
clay_infil_capacity = pd.DataFrame(infiltration, columns=['F']); clay_time_to_infil = pd.DataFrame(infiltration, columns=['F'])
clay_infil_capacity.set_index('F', inplace=True); clay_time_to_infil.set_index('F', inplace=True)

clay_wc = [0, 0.1, 0.2, 0.3, 0.4, .481]

for k in clay_wc:
    Ft = clay_time_to_infil.index.to_list()
    clay_time_to_infil[str(k)] = infil_duration(k, Ft, soil_properties.loc[['clay']])
    clay_infil_capacity[str(k)] = infiltration_capacity(k, Ft, soil_properties.loc[['clay']])

plt.figure(figsize=(8,5))
for k in clay_wc:
    plt.plot(clay_time_to_infil[str(k)], clay_infil_capacity[str(k)], label='initial soil moisture, '+str(k))
    plt.xlabel('Time (seconds)')
    plt.ylabel('Infiltration capacity, fc(t) [cm/s]')
    plt.legend()
    plt.semilogx()
    #plt.ylim(0,.2)
    plt.title('Infiltration capacity for Clay')
# %%
infiltration = np.arange(.05, 10, 0.05)
loam_infil_capacity = pd.DataFrame(infiltration, columns=['F']); loam_time_to_infil = pd.DataFrame(infiltration, columns=['F'])
loam_infil_capacity.set_index('F', inplace=True); loam_time_to_infil.set_index('F', inplace=True)

loam_wc = [0, 0.1, 0.2, 0.3, 0.4, .45]

for k in loam_wc:
    Ft = clay_time_to_infil.index.to_list()
    loam_time_to_infil[str(k)] = infil_duration(k, Ft, soil_properties.loc[['loam']])
    loam_infil_capacity[str(k)] = infiltration_capacity(k, Ft, soil_properties.loc[['loam']])

plt.figure(figsize=(8,5))
for k in loam_wc:
    plt.plot(loam_time_to_infil[str(k)], loam_infil_capacity[str(k)], label='initial soil moisture, '+str(k))
    plt.xlabel('Time (seconds)')
    plt.ylabel('Infiltration capacity, fc(t) [cm/s]')
    plt.legend()
    plt.semilogx()
    #plt.ylim(0,.2)
    plt.title('Infiltration capacity for Loam')
# %%
