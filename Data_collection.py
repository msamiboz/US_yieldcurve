#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:37:22 2024

@author: mehmetsamiboz
"""

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

years_range = range(1990, 2025)


for year in years_range:
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

scaler = StandardScaler(with_std=True, with_mean=True)
res_scaled = scaler.fit_transform(res.loc[:, res.columns != "Date"])
pca_yc=PCA()
pca_yc.fit(res_scaled)

scores = pca_yc.transform(res_scaled)
pca_yc.components_[2]
plt.plot(pca_yc.explained_variance_ratio_,'-bo')


