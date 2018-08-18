import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_gr_D = pd.read_csv('df_gr_D.csv')
df_detailed = pd.read_csv('df_detailed.csv', parse_dates=[0])
df_detailed.index = df_detailed['date']
df_detailed = df_detailed.drop('date', axis=1)
min_vals_df = pd.read_csv('min_vals_df.csv')
min_vals_df = min_vals_df.drop('Unnamed: 0', axis=1)
max_vals_df = pd.read_csv('max_vals_df.csv')
max_vals_df = max_vals_df.drop('Unnamed: 0', axis=1)


def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x == 0 else x for x in values]


df_detailed['CO'] = zero_to_nan(df_detailed['CO'])

plt.plot(min_vals_df['year'], min_vals_df['volume'], 'b')
plt.plot(max_vals_df['year'], max_vals_df['volume'], 'r')
plt.yscale('log')
plt.xlabel('Year')
plt.ylabel('Volume')
plt.show()

# df_gr_M = df_gr_D.groupby(pd.Grouper(freq='M')).transform(np.mean).resample('M').mean()
# df_gr_M = df_gr_M['CO'].fillna(0)

years = []
for i in range(2001, 2019, 2):
    years.append(i)

plt.plot(df_detailed.index, df_detailed['CO'], c='r')
# plt.xticks(years)
plt.xlabel('Year')
plt.ylabel('mg/m3')
plt.title('CO pollution in Madrid 2001-2018')
plt.show()
