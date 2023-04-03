# %%
import os
import numpy as np
import pandas as pd

# %%
# HOMEWORK PROBLEM 1:
P = 0.99    # rainfall in catchment area [m]
Q = 0.33    # runoff in catchment area [m]
Ac = 500    # area of catchment [km2]

E = 1.2     # evaporation of reservoir surface [m]
Ar = 17     # area of reservoir surface [m]

# Water balance
inflow = Q/1000 * Ac        # input [km3]
evaporation = 1.2/1000 * Ar # output [km3]

storage = inflow - evaporation

# Determine available water for nearby community
supply = storage*0.1 * 1e9  # 10% of supply for community [m3]

print('Available water supply for community: {:.3e} m3'.format(supply))

# %%
lat = 32.253460 # latitude of Tucson, in degrees
theta = lat*np.pi/180 # convert deg to rad

radDOYlist = []

day = 1 
while day <= 365:

    delta = 0.4093*np.sin((2*np.pi/365)*day-1.405)

    hs = np.arccos(-np.tan(theta)*np.tan(delta))
    solRJ = 3.7595e7*(hs*np.sin(theta)*np.sin(delta)+np.cos(theta)*np.cos(delta)*np.sin(hs))
    solarRad = solRJ / 86400
    radDOYlist.append(solarRad)
    day += 1

# %%
radSeries = pd.Series(radDOYlist)
ax = radSeries.plot(lw=2, colormap='jet', title='Daily Extraterrestrial Solar Radiation for Tucson')
ax.set(xlabel='Julian Day', ylabel='Solar radiation flux [W/m2]')

# %%
# HOMEWORK PROBLEM 3:
lat = 32.253460 # latitude of Tucson, in degrees
theta = lat*np.pi/180 # convert deg to rad

day = 32 # Feb 1 as Julian Day
delta = 0.4093*np.sin((2*np.pi/365)*day-1.405)

hs = np.arccos(-np.tan(theta)*np.tan(delta))
solRJ = 3.7595e7*(hs*np.sin(theta)*np.sin(delta)+np.cos(theta)*np.cos(delta)*np.sin(hs))
solarRad = solRJ / 86400
print('Daily ET Solar Radiation for Tucson on Feb. 1 =', round(solarRad,2), 'W/m2')

# %%
# HOMEWORK PROBLEM 2:
aridList = [.7, .9]

for i in range(0,2):
    AI = aridList[i]
    runoffCoef = round(np.exp(-AI),2)
    evapCoef = round(1 - runoffCoef,2)
    print('ARIDITY INDEX: {}\nRunoff coefficient: \
           {}\nEvaporation coefficient: {}'.format(AI, runoffCoef, evapCoef))

# %%
# HOMEWORK PROBLEM 4:

alpha = (0.15+0.25)/2       # albedo of a grassy surface
epsilon = (0.97+0.98)/2     # emissivity of a grassy surface
sigma = 5.67e-8             # Stefan-Boltzmann constant [W/m2K4]
Rs = 226.63                 # total incoming solar radiation [W/m2]

K = 273.15                  # Kelvin
Ta = 17.94 + K              # air temperature [K]
RH = 0.66                   # relative humidity
e_s = 20.57                 # saturated vapor pressure @ 17.94 deg. C [hPa]

# Constitutive equations:
e_a = RH*e_s                # partial vapor pressure @ Ta, RH = 0.66
e_ac = 1.24*(e_a/Ta)**(1/7) # atmospheric emissivity for given parameters
Rld = e_ac*sigma*Ta**4      # downward longwave radiation
Rlu = epsilon*sigma*Ta**4   # upward longwave radiation

# Net radiation
Rn = Rs*(1-alpha)+epsilon*Rld-Rlu

print('Net radiation for given conditions is approximately', round(Rn,2), 'W/m2')

# %%
