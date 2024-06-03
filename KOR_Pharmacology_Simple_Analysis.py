# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:14:35 2024

@author: aaron.cone
"""

#%%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pylab as plt
from scipy import stats
import matplotlib.ticker as ticker
from datetime import datetime
import matplotlib.dates as mdates

#%%
### Read csv
df = pd.read_csv('your_path_to_file')


df["RER"] = pd.to_numeric(df.RER, errors='coerce')
df['Hour'] = pd.to_datetime(df['Hour'], errors = 'coerce')

df.rename(columns = {'Subject ID':'Subject_ID'}, inplace = True)

#### Adds XT + XT + Z ###

df['XT+YT+Z'] = df['XT+YT'] + df['Z']


#### Adds XF + YF ###

df['XF+YF'] = df['XF'] + df['YF']

#### Adds XA + YA ###

df['XA+YA'] = df['XA'] + df['YA']



#%%
### separates the groups of animals for treatment days
group_one = df[(df['Subject_ID'] == 'DBH-CRE C75 F0') | (df['Subject_ID'] == 'DBH-CRE C75 F3') | (df['Subject_ID'] == 'DBH-CRE C76 M3') | (df['Subject_ID'] == 'C57 C11 M1') | (df['Subject_ID'] == 'C57 C11 M3') | (df['Subject_ID'] == 'C57 C12 F0') | (df['Subject_ID'] == 'C57 C12 F2')]
# group_two =  df[(df['Subject ID'] == 'DBH-CRE C74 M2') | (df['Subject ID'] == 'DBH-CRE C74 M4') | (df['Subject ID'] == 'DBH-CRE C76 M2') | (df['Subject ID'] == 'C57 C11 M0') | (df['Subject ID'] == 'C57 C11 M2') | (df['Subject ID'] == 'C57 C12 F1')]
group_two =  df[(df['Subject_ID'] == 'DBH-CRE C74 M2') | (df['Subject_ID'] == 'DBH-CRE C74 M4') | (df['Subject_ID'] == 'DBH-CRE C76 M2') | (df['Subject_ID'] == 'C57 C11 M0') | (df['Subject_ID'] == 'C57 C11 M2')]
both_groups = pd.concat([group_one, group_two])


'saline_saline  = saline-u50 (day 1), saline-saline (day2), ntx-u50(day3)'
'saline_u50  = saline-saline (day 1), saline-u50 (day2), ntx-u50(day3)'


### Seperate 
saline_saline = group_one[group_one['Experiment Hour (hrs)'].isin(range(69, 82))]
saline_u50 = group_two[group_two['Experiment Hour (hrs)'].isin(range(69, 81))]
both_groups = both_groups[both_groups['Experiment Hour (hrs)'].isin(range(93, 105))]

day1_g1 = group_one[group_one['Experiment Hour (hrs)'].isin(range(46, 58))]
day1_g2 = group_two[group_two['Experiment Hour (hrs)'].isin(range(46, 58))]
day2_g1 = group_one[group_one['Experiment Hour (hrs)'].isin(range(69, 81))]
day2_g2 = group_two[group_two['Experiment Hour (hrs)'].isin(range(69, 81))]
day3_g1 = group_one[group_one['Experiment Hour (hrs)'].isin(range(93, 105))]
day3_g2 = group_two[group_two['Experiment Hour (hrs)'].isin(range(93, 105))]                                              

u50_comb = pd.concat([day1_g1, day2_g2])
saline_comb = pd.concat([day1_g2, day2_g1])
ntx_u50_comb = pd.concat([day3_g1, day3_g2])



# saline_u50['condition'] = 'Saline + U50,488H'
saline_saline['condition'] = 'Saline + Saline'


u50_comb['condition'] = 'Saline + U50,488H'
saline_comb['condition'] = 'Saline + Saline'


u50_comb['Feed Difference (g)'] = u50_comb['Feed'] - u50_comb.groupby('Subject_ID')['Feed'].transform('first')
saline_saline['Feed Difference (g)'] = saline_saline['Feed'] - saline_saline.groupby('Subject_ID')['Feed'].transform('first')





#%%


all_conditions = pd.concat([saline_comb, u50_comb])


#%%

#Just figure setting
fig, ax = plt.subplots(figsize = (25,10))


# #%%
## PLots Energy Expenditure
sns.lineplot(data = all_conditions, x = 'ThirtyMinute', y = 'H(3)', hue = 'condition', palette=['black', 'red'])
# plt.ylabel('Energy Expenditure (kcal/hr/kg)', fontsize=20)
plt.xlabel('Time (min)', fontsize=20)
# ax.get_legend().set_visible(False)
plt.axvline(x = 4, color = "#000000", ls = '--')
ax.axvspan(20, 25, alpha=0.1, color = "#000000")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.margins(x=0)


#%%

#Just figure setting
fig, ax = plt.subplots(figsize = (25,10))

# ax = plt.gca()

ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.margins(x=0)

# # PLots Locomotion
sns.lineplot(data = all_conditions, x = 'ThirtyMinute', y = 'XY, XT (counts)', hue = 'condition', palette=['black', 'red'])
plt.ylabel('Beam Breaks (counts)', fontsize=20)
plt.xlabel('Time (min)', fontsize=20)
ax.get_legend().set_visible(False)
plt.axvline(x = 4, color = "#000000", ls = '--')
ax.axvspan(20, 25, alpha=0.1, color = "#000000")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.margins(x=0)
#%%

#Just figure setting
fig, ax = plt.subplots(figsize = (25,10))

# #%%
## PLots RER
sns.lineplot(data = all_conditions, x = 'ThirtyMinute', y = 'RER', hue = 'condition', palette=['black', 'red'])
plt.ylabel('RER', fontsize=20)
plt.xlabel('Time (min)', fontsize=20)
ax.get_legend().set_visible(False)
plt.axvline(x = 4, color = "#000000", ls = '--')
ax.axvspan(20, 25, alpha=0.1, color = "#000000")
plt.xticks(fontsize=20)
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.margins(x=0)

#%%
## PLots food intake - CHANGE DATAFRAME TO SALINE_SALINE

# Combines all conditions specifically for feeding
all_conditions_feed = pd.concat([saline_saline, u50_comb])

#Just figure setting
fig, ax = plt.subplots(figsize = (25,10))

sns.lineplot(data = all_conditions_feed, x = 'ThirtyMinute', y = 'Feed Difference (g)', hue = 'condition', palette=['black', 'red'])
plt.ylabel('Food Intake (g)', fontsize=20)
plt.xlabel('Time (min)', fontsize=20)
# ax.get_legend().set_visible(False)
plt.axvline(x = 4, color = "#000000", ls = '--')
ax.axvspan(20, 25, alpha=0.1, color = "#000000")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.margins(x=0)
