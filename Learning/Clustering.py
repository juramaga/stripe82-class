
# coding: utf-8

# In[ ]:

import os
os.chdir('..')


# In[ ]:

import pandas as pd
d = pd.read_csv('FeatureExtraction/feature_matrix.csv',header=0,sep=',')
del d['Unnamed: 0']
d = d.dropna()
d.head()


# In[ ]:

one_hot = pd.get_dummies(d.ix[:,1])
d=d.drop('Color',axis=1)
d = d.join(one_hot)
d.head()


# In[ ]:

from sklearn.cluster import KMeans
import numpy as np
X = d.ix[:,1:7]
Y = X.values
Y


# ### Hierarchical Clustering and Dendrogram Plotting

# In[ ]:

import fastcluster
Z = fastcluster.linkage(Y, method="ward")


# In[ ]:

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
get_ipython().magic(u'matplotlib inline')


# In[ ]:

plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()


# In[ ]:

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata


# In[ ]:

# set cut-off based on maximum distance from the plotted dendrogram
max_d = 150  # max_d as in max_distance


# In[ ]:

fancy_dendrogram(
    Z,
    truncate_mode='lastp',
    p=12,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=10,
    max_d=max_d,  # plot a horizontal cut-off line
)
plt.show()


# ### Viewing the Clusters

# In[ ]:

from scipy.cluster.hierarchy import fcluster
max_d = 95
clusters = fcluster(Z, max_d, criterion='distance')
clusters
X['Labels'] = clusters
g = X.groupby(['Labels'])
g.groups

