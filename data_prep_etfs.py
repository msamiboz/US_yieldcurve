import pandas as pd

# Read the CSV file
date= pd.read_csv('etf_data/SHY.csv')['Date']
shy = pd.read_csv('etf_data/SHY.csv')['Close/Last']
shy.name = "SHY"
shy.index = date

iei = pd.read_csv('etf_data/IEI.csv')['Close/Last']
iei.name = "IEI"
iei.index = date

tlh = pd.read_csv('etf_data/TLH.csv')['Close/Last']
tlh.name = "TLH"
tlh.index = date

agg = pd.read_csv('etf_data/GOVT.csv')['Close/Last']
agg.name = "GOVT"
agg.index = date

cbind = pd.concat([shy, iei, tlh, agg], axis=1)

cbind.index = pd.to_datetime(cbind.index)
cbind = cbind.sort_index()

cbind.to_csv('etf_data/all_etfs.csv', index=True)