# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
# Create a dataframe of climate data from the homework
df = pd.DataFrame({'month': [1,2,3,4,5,6,7,8,9,10,11,12],
                   'P': [135,131,155,122,114,103,121,115,93,90,99,125],
                   'E': [24,34,56,79,112,124,121,103,71,47,29,23],
                   'Q': [58,62,79,72,55,39,34,30,28,32,37,50]})

# %%
# Complete the monthly water balance for the catchment by calculating the change in storage
df['dS'] = df['P']-df['E']-df['Q']

df.loc[-1] = [0, np.nan, np.nan, np.nan, np.nan] # add row for interannual storage value
df.index = df.index + 1
df = df.sort_index()
df['month'] = df['month'].astype('int') # correct month col number type

# %%
# Calculate the storage for the water balance
df['S'] = np.zeros(13) # add column and fill with zeroes
df.iat[0,-1] = 200     # take value from homework assignment of carryover

for i in range(1,13):
    df.iat[i,-1] = df.iat[i-1,-1] + df.iat[i,-2]

df.set_index('month')

# %%
# Construct Wundt diagram from calculated metrics
metrics = df.columns[1:]

fig, ax = plt.subplots()
ax.set_xlim(1,12)
plt.xticks(np.arange(1,13, step=1))

for i in metrics:
    df[i][1:].plot(marker='.')

plt.xlabel('Month')
plt.ylabel('Average Water Balance Comp. (mm/month)')
plt.legend(loc='upper right', ncol=2)
plt.title('Wundt Diagram of Georgia Catchment')

# %%
# PROBLEM 2:
dfSnow = pd.read_excel('snowPitData_hw2.xlsx', sheet_name='data')
dfSnow['depth_mid'] = dfSnow['Depth_t'] - 5

# %%
keyList = ['south_25', 'south_75', 'center', 'north_75', 'north_25']
snowDict = {key: dfSnow[dfSnow['location']==key] for key in keyList}
# %%
fig, ax = plt.subplots(1,5)

for key in keyList:
    snowDict[key].plot(x='Density', y='depth_mid')
    plt.title(key)
# %%
fig = plt.figure()
fig.subplots_adjust(hspace=.2,wspace=0.2)

for i in range(0,5):
    key = keyList[i]
    ax = fig.add_subplot(1,5,i+1)
    x = snowDict[key].Density
    y = snowDict[key].depth_mid

    ax.plot(x,y)

    ax.set_title(key)

    plt.ylim(0,110)
    plt.xticks(np.arange(0,350, step=150))
    #plt.subplots(figsize=(2,3))
plt.tight_layout(pad=1)
# %%
fig, ax = plt.subplots(1,5, sharex=True, sharey='row', figsize=(6,4))



for i in range(0,5):
    key = keyList[i]
    x = snowDict[key].Density
    y = snowDict[key].depth_mid
    ax[i].plot(x,y)
    ax[i].set_title(key)

    #plt.ylim(0,110)
    #plt.xticks(np.arange(0,350, step=150))

fig.text(0.5, 0.001, 'Density of snow (kg/m3)', ha='center')
fig.text(0.001, 0.5, 'Depth above ground (cm)', va='center', rotation='vertical')
fig.text(0.5, 0.99, 'Density profile of snow columns', ha='center')
fig.tight_layout(pad=1)

# %%
