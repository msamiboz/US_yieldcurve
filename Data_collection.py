#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:37:22 2024

@author: mehmetsamiboz
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

years_range = range(1990, 2025)


for year in years_range:
    print(year)
    path = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"+str(year)+"/all?type=daily_treasury_yield_curve&field_tdr_date_value="+str(year)+"&page&_format=csv"
    data = pd.read_csv(path)
    if year == 1990:
        res = data
    else:
        res = pd.concat([res,data])
        

cols = ['Date', '1 Mo', '2 Mo', '3 Mo', '4 Mo', '6 Mo', '1 Yr', '2 Yr', '3 Yr', '5 Yr', '7 Yr', '10 Yr','20 Yr', '30 Yr']
res = res[cols]
res['Date'] = pd.to_datetime(res['Date'])
res = res.sort_values(by='Date').reset_index(drop=True)
res = res.drop(["2 Mo","4 Mo"],axis=1).dropna()
#####

res.to_csv("US_yieldcurve.csv")
x=0
#####
res = pd.read_csv("US_yieldcurve.csv")
del res[res.columns[0]]
res = res.loc[res["Date"]>"2007-01-03"]

returns_df = pd.DataFrame({'Date': res['Date']})  # Initialize DataFrame with 'Date' column

for col in res.columns[1:]:  # Exclude 'Date' column
    returns_df[col] = (res[col].shift(-1) - res[col]) / res[col]

# Drop the last row as it will contain NaN values
returns_df = returns_df[:-1]
res = returns_df.sort_values(by='Date')
scaler = StandardScaler(with_std=True, with_mean=True)
res_scaled = scaler.fit_transform(res.loc[:, res.columns != "Date"])
pca_yc=PCA()
pca_yc.fit(res_scaled)

scores = pca_yc.transform(res_scaled)
pca_yc.components_
plt.bar(range(len(pca_yc.explained_variance_ratio_)),pca_yc.explained_variance_ratio_*100)
plt.xlabel('Components')
plt.ylabel('Ratio (%)')
plt.title('Explained Variance Ratio of the Components')
plt.show()
#if you want to save call it before plt.show
plt.savefig("EVR.jpeg",dpi=400)

plotdat = pca_yc.components_[[0,1,2]]
tick_labels = res.columns.values[1:]
plt.imshow(plotdat, cmap='viridis', interpolation='nearest')
plt.xticks(np.arange(len(tick_labels)), tick_labels)
plt.xlabel('Time to Maturity')
plt.ylabel('Components')
plt.title('Heatmap of Components')
plt.show()
#if you want to save call it before plt.show
plt.savefig("heatmap.jpeg",dpi=400)

interest_rates = res.iloc[:, 1:].values
loading1= pca_yc.components_[0]
result1 = np.dot(interest_rates, loading1)
loading2= pca_yc.components_[1]
result2 = np.dot(interest_rates, loading2)
loading3= pca_yc.components_[2]
result3 = np.dot(interest_rates, loading3)

output_pca = pd.DataFrame({"Date":res.Date.values,"Comp1":result1, "Comp2":result2, "Comp3":result3})

plt.plot(output_pca['Date'], output_pca['Comp1'], label='Component 1')
plt.plot(output_pca['Date'], output_pca['Comp2'], label='Component 2')
plt.plot(output_pca['Date'], output_pca['Comp3'], label='Component 3')

plt.title('PCA Components over Time')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()
plt.grid(True)

plt.show()

output_pca.to_csv('pca_components.csv', index=False)

weigths = pca_yc.explained_variance_[[0,1,2]]
plotdat[0][[4,6,8]] * weigths[0] *-1 + plotdat[1][[4,6,8]]*weigths[1] + plotdat[2][[4,6,8]] * weigths[2]