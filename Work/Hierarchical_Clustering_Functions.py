#This function will return a denorogram and heat map for the given dataset using agglomerative hierarchical clustering with complete linkage. This means that
#we'll start with all states as their own clusters then iteratively combine clusters (the agglomerative part) with the minimum distance between the most dissimilar members of any two
#clusters (the complete linkage part).0
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

def hierarchical_clust(input_df):
    input_df = input_df.set_index(input_df['State'])
    input_df = input_df.drop('State', axis=1)

    row_clusters = linkage(input_df.values,
                                            method = 'complete',
                                            metric = 'euclidean')

    #Now we want to create a dendrogram and heat map for the hierarchical clustering
    #Instantiate a figure object. The figure size and the position of the axes were chosen by trial and error
    fig = plt.figure(figsize = (8,8))
    axd = fig.add_axes([0.09, 0.1, 0.2, 0.6])
    #Create dendrogram from row_clusters

    row_dendr = dendrogram(row_clusters,
                                            orientation = 'right'
                                            ,labels = input_df.index)

    #The dendrogram object, row_dendr creates cluster labels and those are stored in the 'leaves' list. Since we're putting the dendrogram on the vertical axis, we want to reverse the order of those labels.
    #Extended slicing  [a:b:c] will return members of the the list starting at a, stopping at b, indexing by c. If c is negative, then by default a = -1 and b =0. So [::-1] will reverse the order of
    #a list

    df_rowclust = input_df.ix[row_dendr['ivl'][::-1]]

    #Construct the heat map
    axm = fig.add_axes([0.33, 0.1, 0.6, 0.6]);
    cax = axm.matshow(df_rowclust,
                                    aspect = 'auto',
                                    interpolation = 'nearest',
                                    cmap = 'hot_r')
    axd.set_xticks([])
    # axd.set_yticks([])
    # for i in axd.spines.values():
    #     i.set_visible(False)
    fig.colorbar(cax)
    axm.set_xticklabels([' '] + list(df_rowclust.columns))
    axm.set_yticklabels([' '])
    # axm.set_yticklabels([' '] + list(df_rowclust.index))
    plt.show()



def hierarchical_clust_var(input_df, var, linkage_matrix):
    input_df = input_df.set_index(input_df[var])
    input_df = input_df.drop(var, axis=1)

    print('\n 2')

    #Now we want to create a dendrogram and heat map for the hierarchical clustering
    #Instantiate a figure object. The figure size and the position of the axes were chosen by trial and error
    fig = plt.figure(figsize = (8,8))
    axd = fig.add_axes([0.09, 0.1, 0.2, 0.6]) #space from left, space from bottom, width, height
    #Create dendrogram from row_clusters

    '''
    row_dendr = dendrogram(row_clusters,
                                            orientation = 'right'
                                            ,labels = input_df.index)
    '''

    print('\n 3')
    row_dendr = dendrogram(linkage_matrix
                          ,orientation = 'right'
                          ,labels = input_df.index);

    #Labeling the graph
    plt.tick_params(\
      axis = 'x',          # changes apply to the x-axis
      which = 'both',      # both major and minor ticks are affected
      bottom = 'off',      # ticks along the bottom edge are off
      top = 'off',         # ticks along the top edge are off
      labelbottom = 'off')

    #The dendrogram object, row_dendr creates cluster labels and those are stored in the 'leaves' list. Since we're putting the dendrogram on the vertical axis, we want to reverse the order of those labels.
    #Extended slicing  [a:b:c] will return members of the the list starting at a, stopping at b, indexing by c. If c is negative, then by default a = -1 and b =0. So [::-1] will reverse the order of
    #a list

    df_rowclust = input_df.ix[row_dendr['ivl'][::-1]]
    print('\n 4')
    #Construct the heat map
    axm = fig.add_axes([0.33, 0.1, 0.6, 0.6]) #space from left, space from bottom, width, height
    cax = axm.matshow(df_rowclust,
                                    aspect = 'auto',
                                    interpolation = 'nearest',
                                    cmap = 'hot_r')
    axd.set_xticks([])
    # axd.set_yticks([])
    # for i in axd.spines.values():
    #     i.set_visible(False)
    fig.colorbar(cax)
    axm.set_xticklabels([' '] + list(df_rowclust.columns))
    axm.set_yticklabels([' '])
    # axm.set_yticklabels([' '] + list(df_rowclust.index))
    plt.show()