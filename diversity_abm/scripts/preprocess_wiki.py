from gensim.models import Word2Vec
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from matplotlib import pyplot as plt 
from utils import euclidean_distance

#model = Word2Vec.load('../models/wiki.en.word2vec.model')
animals = pd.read_csv('../models/animal_list.csv')

#df = pd.DataFrame()
#for a in animals.Animals:
#    v = model.wv.get_vector(a)
#    df[a] = v

#df.T.to_csv('../models/wiki_vectors.tsv', sep='\t', header=False)
df = pd.read_csv('../models/wiki_vectors.tsv', sep='\t', header=None,
                 index_col=0)

# PCA and plot
X_scaled = MinMaxScaler().fit_transform(df.values)
pca = PCA(n_components=2) # added components
X_scaled = pca.fit_transform(X_scaled) # added transform

# Make scree plot
cvar = pca.explained_variance_ratio_
sns.barplot(x=['comp_' + str(v) for v in range(len(cvar))], 
            y=cvar, color='darkred')
plt.xticks(rotation=90)
plt.show()

# Use scaled version
idx = df.index
df = pd.DataFrame(X_scaled)
df.index = idx
df = pd.read_csv('../models/wiki_vectors_small.tsv', sep='\t', header=None,
                 index_col=0) # added

# Compute euclidean distances
emat = euclidean_distance(df, animals) / 30 #400
sns.histplot(np.tril(emat, k=-1).ravel()[np.tril(emat, k=-1).ravel()!=0])
plt.title('L2 norm values')
plt.show()

emat.to_csv('../models/wiki_euclidean_distance_small.tsv', sep='\t')

# Position in vector space is normalized on a scale from 0 to 1
# Original distance matrix has values up to 400
# Distance matrix is normalized by maximum value (sums to 1)


''' 
# TODO: try play with dimensionality reduction
import itertools
from sklearn.metrics.pairwise import euclidean_distances

combs = itertools.combinations(range(df.shape[1]), 10)
combs20 = itertools.combinations(range(df.shape[1]), 20)
combs50 = itertools.combinations(range(df.shape[1]), 50)
combs100 = itertools.combinations(range(df.shape[1]), 100)
combs200 = itertools.combinations(range(df.shape[1]), 200)
combs400 = itertools.combinations(range(df.shape[1]), 400)

def _sampling(iterator, every=1000000):
    combs_all = []
    i = 0
    while i < (every*100):
        el = next(iterator)
        if i % every == 0:
            combs_all.append(el)
        i += 1
    return combs_all

combs = _sampling(combs)
combs20 = _sampling(combs20)
combs50 = _sampling(combs50)
combs100 = _sampling(combs100)
combs200 = _sampling(combs200)
combs_all = combs + combs20 + combs50 + combs100 + combs200 + list(combs400)

res = []
for idx, i in enumerate(combs_all):
    etemp = euclidean_distances(df.iloc[:,list(i)], df.iloc[:,list(i)])
    nz = np.tril(etemp, k=-1).ravel()
    vals = nz[nz!=0]
    res.append((len(i), i, idx, np.mean(vals), np.std(vals)))
ddf = pd.DataFrame(res, columns=['n_features', 'indices', 'index', 'mean', 'std'])
ddf = ddf.sort_values(by='std', ascending=False)

'''