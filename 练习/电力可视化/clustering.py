import numpy as np
from sklearn.manifold import TSNE
import csv
import pandas as pd

f = open(r'TSNE.csv', encoding='utf-8')
df = pd.read_csv(f)
data = df.iloc[:, :].values

tsne = TSNE(n_components=2)
Coor = tsne.fit_transform(data)
print(Coor)
# print(tsne.embedding_)

np.savetxt('Tsne-coor.csv', Coor, delimiter = ',')