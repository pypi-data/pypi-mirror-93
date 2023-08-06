import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing
from scipy import stats


data = pd.read_csv('dataset/orders.csv')[['city_name_fa']]
counts = data.groupby(data.columns.tolist(),as_index=False).size()
counts.columns = ['city', 'Shopping_count']


xsCity=[]
sCity=[]
mCity=[]
lCity=[]
xlCity=[]
xxlCity=[]
for index, row in counts.iterrows():
    if row['Shopping_count']<10:
        xsCity.append(row['city'])
    elif row['Shopping_count']<100:
        sCity.append(row['city'])
    elif row['Shopping_count']<500:
        mCity.append(row['city'])
    elif row['Shopping_count']<1000:
        lCity.append(row['city'])
    elif row['Shopping_count']<10000:
        xlCity.append(row['city'])
    else:
        xxlCity.append(row['city'])
        
print('there are '+str(len(xsCity))+' cities with less than 10 purchases')
print('\n\n\n')

print('there are '+str(len(sCity))+' cities with 11 to 100 purchases')
print('\n\n\n')

print('there are '+str(len(mCity))+' cities with 101 to 500 purchases')
print(mCity)
print('\n\n\n')

print('there are '+str(len(lCity))+' cities with 501 to 1000 purchases')
print(lCity)
print('\n\n\n')

print('there are '+str(len(xlCity))+' cities with 1001 to 10000 purchases')
print(xlCity)
print('\n\n\n')

print('there are '+str(len(xxlCity))+' cities with more than 10000 purchases')
print(xxlCity)
print('\n\n\n')



