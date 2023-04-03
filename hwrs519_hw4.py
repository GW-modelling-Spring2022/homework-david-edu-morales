# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearson3

# %%
'''PROBLEM #1 (part one)'''
# store the max flow and associated years in two arrays
year = np.arange(1949, 2011, 1)
max_flow = np.array([334.1,29.4,586.2,1319.6,108.2,665.4,120.1,33.4,131.7,444.6,
                     1183.6,693.8,34.5,166.2,184.3,53.2,1277.1,297.3,328.5,328.5,
                     139.9,235.6,532.4,1526.3,421.9,109.0,164.2,261.9,54.4,2186.1,
                     787.2,1701.8,62.3,267.3,1393.2,1036.4,526.7,184.9,150.1,235.9,
                     53.2,444.6,1322.4,535.2,2525.9,260.8,637.1,59.7,87.8,171.3,
                     103.9,97.4,70.2,95.4,226.3,174.1,869.3,224.6,243.8,1373.4,
                     77.0,1356.4])

# number of years
num_years = np.shape(max_flow)[0]

# sort max flow values
sorted_max_flow = np.sort(max_flow)

# Use Gringorten formula to calculate the probabilities:
# Pm = m - 0.44 / n + 0.12, where m = position & n = sample size
gringorten_p = np.zeros(num_years)

for k in range(num_years):
    gringorten_p[k] = (k+1 - 0.44)/(num_years + 0.12)

# Calculate return period
T = 1/(1-gringorten_p)

# Calculate the rduced vairable (Gumbel)
y_T = -np.log(np.log(T/(T-1)))

# %%
'''Problem #1 (part two)'''
# Construct figures to plot the data

# set up the figure (containing two subplots)
fig, axes = plt.subplots(1,2,
                         constrained_layout=True,
                         figsize=(9,3)
                         )

# Plot the data
axes[0].plot(gringorten_p, sorted_max_flow, label='empirical data', marker='.')
axes[1].plot(y_T, sorted_max_flow)

# axis labels
axes[0].set_ylabel('maximum daily flow [m$^3$ s$^-1$]')
axes[0].set_xlabel('cumulative probability')
axes[1].set_xlabel('return period [year]')

# set limits of the different axes
axes[0].set_ylim([0,3000]); axes[1].set_ylim([0,3000])
axes[0].set_xlim([0,1])

# the x-axis of the second subplot (axes[1]) is the reduced variable y_T,
# this variable is related to the return period T
# we now manually set the x-axis ticks to specific return periods
# and calculate the correct corresponding axis locations for these return periods:

# define return periods:
T_list = np.array([2,5,10,25,50,100])
T_list_str = ['2','5','10','25','50','100']

# calc reduced variable for these return periods and set them as tick locations:
axes[1].set_xticks(-np.log(np.log(T_list/(T_list-1))))

# label the tick locations:
axes[1].set_xticklabels(T_list_str)

# add grid and legend to the plots
axes[0].grid(); axes[1].grid()
axes[0].legend()

# %%
'''Problem one, figure one'''
# set up the figure (containing two subplots)
fig, axes = plt.subplots(constrained_layout=True,
                         figsize=(4.5,3)
                         )

# Plot the data
axes.plot(gringorten_p, sorted_max_flow, label='observations', color='red')

# axis labels
axes.set_ylabel('Max streamflow [m3/s]')
axes.set_xlabel('Cumulative probability')

# set limits of the different axes
axes.set_ylim([0,3000])
axes.set_xlim([0,1])

# add grid and legend to the plots
axes.grid()
axes.legend()

# %%
'''Problem one, figure two'''
# set up the figure (containing two subplots)
fig, axes = plt.subplots(constrained_layout=True,
                         figsize=(4.5,3)
                         )

# Plot the data
axes.plot(y_T, sorted_max_flow, label='obseravtions', color='black')

# axis labels
axes.set_ylabel('Max streamflow [m3/s]')
axes.set_xlabel('Return period [years]')

# set limits of the different axes
axes.set_ylim([0,3000])

# the x-axis of the second subplot (axes[1]) is the reduced variable y_T,
# this variable is related to the return period T
# we now manually set the x-axis ticks to specific return periods
# and calculate the correct corresponding axis locations for these return periods:

# define return periods:
T_list = np.array([2,5,10,25,50,100])
T_list_str = ['2','5','10','25','50','100']

# calc reduced variable for these return periods and set them as tick locations:
axes.set_xticks(-np.log(np.log(T_list/(T_list-1))))

# label the tick locations:
axes.set_xticklabels(T_list_str)

# add grid and legend to the plots
axes.grid()
axes.legend()

# %%
'''ACTUALLY USED FOR HOMEWORKS SUBMISSION'''
# set up the figure (containing two subplots)
fig, axes = plt.subplots(constrained_layout=True,
                         figsize=(4.5,3),
                         )

# Plot the data
axes.plot(gringorten_p, sorted_max_flow, label='empirical data', marker='.', color='red')

# axis labels
axes.set_ylabel('maximum daily flow [m$^3$ s$^-1$]')
axes.set_xlabel('cumulative probability')
axes.set_title('Empirical probability plot for Salt River, AZ')


# set limits of the different axes
axes.set_ylim([0,3000])
axes.set_xlim([0,1])

# the x-axis of the second subplot (axes[1]) is the reduced variable y_T,
# this variable is related to the return period T
# we now manually set the x-axis ticks to specific return periods
# and calculate the correct corresponding axis locations for these return periods:

# define return periods:
T_list = np.array([2,5,10,25,50,100])
T_list_str = ['2','5','10','25','50','100']

# add grid and legend to the plots
axes.grid()
axes.legend()

# %%
'''Problem 2'''
# Determine the frequency curve comprising the estimated flood magnitudes for
# return periods of 2, 5, 10, 25, 50, and 100 years using the EVI (Gumbel)
# distribution. Compare the fitted distribution to the plotted data obtained
# in problem 1.

# Calculate mu and alpha for the Gumbel distro:
# mu = mean - 0.5772alpha
# alpha = sqrt(6)STD/pi

sigma = np.std(sorted_max_flow, ddof=1)
mean = np.mean(sorted_max_flow)

alpha = np.sqrt(6)*sigma/np.pi
mu = mean - 0.5772*alpha

print('alpha: {:.2f}'.format(alpha), '\n'
      'mu: {:.2f}'.format(mu)      
      )

# The extreme value for return period T can now be calculated as:
# x_T,gumbel = mu + alpha(y_T,gumbel)
# y_T,gumbel = -ln[ln(T/T-1)]

# The corresponding probability is then:
# P_T,gumbel = exp[-exp(-y_T,gumbel)] = T-1/T

# T_list was defined before as the years 2, 5, 10, 25, 50, 100
# Calculate the corresponding reduced variable
y_T_list = -np.log(np.log(T_list/(T_list-1)))
gumbel_flow = mu + alpha * y_T_list

gumbel_p = np.exp(-np.exp(-y_T_list))

# the probability can calso be calculated as gumbel_p = (T_list-1/T_list)

print('return period:', T_list,'\n'
      'Gumbel flood magnitude:', np.round(gumbel_flow,1))

# %%
# same plots as before, but now with Gumbel
fig, axes = plt.subplots(constrained_layout=True,
                         figsize=(4.5,3)
                         )
axes.plot(gringorten_p, sorted_max_flow, label='observations', color='red')
axes.plot(gumbel_p, gumbel_flow, label='Gumbel', color='blue')


axes.set_ylim([0,3000])
axes.set_xlim([0,1])
axes.set_ylabel('Max streamflow [m3/s]')
axes.set_xlabel('Cumulative probability')

axes.grid()
axes.legend()

# %%
'''Problem 2 graph b'''
fig, axes = plt.subplots(constrained_layout=True,
                         figsize=(4.5,3)
                         )

axes.plot(y_T, sorted_max_flow, label='observations', color='red')
axes.plot(y_T_list, gumbel_flow, label='Gumbel', color='blue')

axes.set_ylim([0,3000])
axes.set_ylabel('Max streamflow [m3/s]')
axes.set_xlabel('Return period [years]')

# scale the x ticks
axes.set_xticks(-np.log(np.log(T_list/(T_list-1))))
axes.set_xticklabels(T_list_str)

axes.grid()
axes.legend()
# %%
'''Problem 3: Water Resources Council Method (part one)'''
# calculate log transformed flow, mean, and std
log_flows = np.log10(sorted_max_flow)
log_mean = np.mean(log_flows)
log_std = np.std(log_flows, ddof=1)

print('log transformed flow mean: {:.2f}'.format(log_mean),'\n'
      'log transformed flow std: {:.2f}'.format(log_std))

# calculate skewness of data:
C_s = num_years * np.sum(np.power(log_flows-log_mean, 3)) / ((num_years-1)*(num_years-2)*log_std**3)

print('C_s: {:.3f}'.format(C_s))

# choose the correct calculation of A and B depending on C_s:
if abs(C_s) <= 0.9:
    A = -0.33 + 0.08 * abs(C_s)
else:
    A = -0.52 + 0.30 * abs(C_s)

if abs(C_s) <= 1.5:
    B = 0.94 - 0.26 * abs(C_s)
else:
    B = 0.55


VC_s = np.power(10, A-B*np.log10(num_years/10))

print('V(C_s): {:.3f}'.format(VC_s))

# mapped skewness and variance
C_m = -0.1
VC_m = 0.303

# calculate weighted skewness
C_w = (VC_m * C_s + VC_s * C_m)/(VC_m + VC_s)

print('C_w: {:.3f}'.format(C_w))

# The K_T values can now be taken from the provided table:
K_T = pearson3.ppf(1-1/T_list, C_w)
print(K_T)

# Calculate pearson reduced variable
y_T_pearson = log_mean + K_T * log_std
# note: y_T_pearson is a different reduced variable but still refers to times T

# calculate pearson extreme flow
pearson_flow = np.power(10, y_T_pearson)

# calculate probability
# this is still based on the same return period
pearson_p = (T_list - 1) / T_list

print('return period:', T_list, '\n'
      'Pearson3 flood magnitude:', np.round(pearson_flow, 1))

# %%
'''Problem #3 (part two)'''
# same plot as before but now with Gumbel and log-pearson iii
fig, axes = plt.subplots(constrained_layout=True,
                         figsize=(4.5,3)
                         )

axes.plot(gringorten_p, sorted_max_flow, label='observations', marker='.', color='red')
axes.plot(gumbel_p, gumbel_flow, label='Gumbel', color='blue')
axes.plot(pearson_p, pearson_flow, label='log-Pearson3', color='k')

axes.set_ylim([0,3000])
axes.set_xlim([0,1])
axes.set_ylabel('Max streamflow [m3/s]')
axes.set_xlabel('Cumulative probability')
axes.grid()
axes.legend()

# %%
# same plot as before but now with Gumbel and log-pearson iii
fig, axes = plt.subplots(constrained_layout=True,
                         figsize=(4.5,3)
                         )

axes.plot(y_T, sorted_max_flow, label='observations', marker='.', color='red')
axes.plot(y_T_list, gumbel_flow, label='Gumbel', color='blue')
axes.plot(y_T_list, pearson_flow, label='log-Pearson3', color='k')

axes.set_ylim([0,4100])
axes.set_ylabel('Max streamflow [m3/s]')
axes.set_xlabel('return period [years]')

axes.set_xticks(-np.log(np.log(T_list/(T_list-1))))
axes.set_xticklabels(T_list_str)

axes.grid()
axes.legend()
# %%
