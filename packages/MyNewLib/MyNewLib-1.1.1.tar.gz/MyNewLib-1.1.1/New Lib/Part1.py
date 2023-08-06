import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing
from scipy import stats

data = pd.read_excel('dataset/keifiat.xlsx')
data = data[['product_id','likes', 'dislikes']]


data2 = pd.read_csv('dataset/tarikhche kharid.csv')[['product_id']]
counts = data2.groupby(data2.columns.tolist(),as_index=False).size()
counts.columns = ['product_id', 'Shopping_Count']


result = pd.merge(data, counts, how='left', on=['product_id'])
result.loc[~result.product_id.isin(data2.product_id), 'Shopping_Count'] = 0
result = result[['likes','dislikes','Shopping_Count']]



result = result[(np.abs(stats.zscore(result)) < 3).all(axis=1)]
x = result.values 
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
result = pd.DataFrame(x_scaled)
result.columns = ['likes','dislikes','Shopping_Count']



def doKmeans(X, nclust=2):
    model = KMeans(nclust)
    model.fit(X)
    clust_labels = model.predict(X)
    cent = model.cluster_centers_
    return (clust_labels, cent)

clust_labels, cent = doKmeans(result,6)
kmeans = pd.DataFrame(clust_labels)
data.insert((result.shape[1]),'kmeans',kmeans)



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(result['likes'],result['dislikes'],result['Shopping_Count'],
                     c=kmeans[0])
ax.set_title('Mahboubiyat Kalaha')
ax.set_xlabel('likes')
ax.set_ylabel('dislikes')
ax.set_zlabel('Shopping_Count')
plt.colorbar(scatter)


plt.show()
