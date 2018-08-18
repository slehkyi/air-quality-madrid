import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

with pd.HDFStore('madrid.h5') as data:
    df_stations = data['master']

with pd.HDFStore('madrid.h5') as data:
    test = data['28079016']

test.rolling(window=24).mean().plot(figsize=(20, 7), alpha=0.8)
plt.show()

partials = list()

with pd.HDFStore('madrid.h5') as data:
    stations = [k[1:] for k in data.keys() if k != '/master']
    for station in stations:
        df = data[station]
        df['station'] = station
        partials.append(df)

df = pd.concat(partials).sort_index()

df = df.fillna(0)

one_station = df[df['station']=='28079017']
x = one_station.index.to_series()

mean_values = np.array([])
for i in range(len(x)):
    val = df['CO'][df.index == x[i]].mean()
    mean_values = np.append(mean_values, val)
    if i % 100 == 0:
        print('Iteration number: ' + str(i))

df_mean = pd.DataFrame(data=mean_values, index=x, columns=['CO'])
df_mean.to_csv('CO_mean_values.csv')

df_mean = df_mean.fillna(0)
df_gr_D = df_mean.groupby(pd.Grouper(freq='D')).transform(np.mean).resample('D').mean()
df_gr_D = df_gr_D.fillna(0)
df_gr_M = df_gr_D.groupby(pd.Grouper(freq='M')).transform(np.mean).resample('M').mean()
df_gr_M = df_gr_M['CO'].fillna(0)

df_detailed = df_gr_D.copy()
df_detailed['year'] = df_detailed.index.year
df_detailed['month'] = df_detailed.index.month
df_detailed['day'] = df_detailed.index.day
df_detailed = df_detailed.fillna(0)

max_vals_df = pd.DataFrame(columns=['year', 'month', 'volume'])
for i in range(2001, 2019):
    max_val = max(df_detailed['CO'][df_detailed['year'] == i])
    if max_val > 0.0:
        month = df_detailed[(df_detailed['CO'] == max_val) & (df_detailed['year'] == i)]['month'].values[0]
        to_add = pd.DataFrame([[i, month, max_val]], columns=['year', 'month', 'volume'])
        max_vals_df = max_vals_df.append(to_add)

min_vals_df = pd.DataFrame(columns=['year', 'month', 'volume'])
for i in range(2001, 2019):
    min_val = min(df_detailed['CO'][df_detailed['year'] == i])
    if min_val > 0.0:
        month = df_detailed[(df_detailed['CO'] == min_val) & (df_detailed['year'] == i)]['month'].values[0]
        to_add = pd.DataFrame([[i, month, min_val]], columns=['year', 'month', 'volume'])
        min_vals_df = min_vals_df.append(to_add)

max_vals_df.to_csv('max_vals_df.csv')
min_vals_df.to_csv('min_vals_df.csv')
df_detailed.to_csv('df_detailed.csv')
df_gr_D.to_csv('df_gr_D.csv')




