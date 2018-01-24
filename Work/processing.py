  
def processing(df):

  import numpy as np
  import pandas as pd
  import array
  import random
  import nltk
  import re
  import os
  import time
  import codecs
  import matplotlib.pyplot as plt
  from sklearn import feature_extraction
  from scipy.spatial.distance import pdist
  from collections import Counter
  from scipy.cluster.hierarchy import average, dendrogram, fcluster, linkage

  #Functions Stephen wrote
  from Hierarchical_Clustering_Functions import hierarchical_clust, hierarchical_clust_var

  #Chars that were selected to use, major chars minus top 10 objectionable ones
  columns = [
            'YrsLic'
            ,'NumVeh' 
            ,'PriorBI' 
            ,'YwP' 
            ,'Source' 
            ,'Accidents' 
            ,'NumDriv'
            ]

  #Limit our columns down to the ones that we need and change data type
  df_min = df[columns]
  df2 = pd.DataFrame(np.array(df_min.as_matrix()))
  print('Data Formatted!')
  print('\n')

  #Calculate our linakge matrix / UPGMA calculation
  simmatrix = pdist(df2)
  linkage_matrix = linkage(simmatrix, method = 'average')
  print('Linkage Calculated!')
  print('\n')

  #Make a while loop that makes sure we get 5 clusters 
  Clusters = 0 #check to make sure there are 5
  Last_Clusters = 10000 #initial check to make sure we don't get in an infinite loop
  Threshold = round(.5*simmatrix.max(),1) #Starting point for clusters
  Last_Threshold = 10000
  Threshold_2back = 10000
  Differential = 1

  #Make sure everything was initialized correctly
  print('The cut off is here' , Threshold) 
  print('The cut off last time was', Last_Threshold)
  print('The cut off two times back was', Threshold_2back)
  print('The number of clusters is', Clusters)
  print('The number of clusters last time was', Last_Clusters)
  print('The differential is', Differential)
  print('\n')

  #We have 5 occupation groups currently, so let's assume we want to replace those and hunt for a better 5
  while Clusters != 5:

    #This writes the cluster number to the data on each row
    ind = np.array(fcluster(linkage_matrix, Threshold, 'distance')) #.5*simmatrix.max()
    
    #Logic to adjust threshold value
    Clusters = ind.max() 
    if Clusters < 5:
      Threshold = round(Threshold - Differential , 5) #if there are not enough clusters, we need less branch distance #FIX THE THING WITH DIMINISHING RETURNS ZONING
    elif Clusters > 5:
      Threshold = round(Threshold + Differential , 5) #if there are too many clusters, we need more branch distance

    #Update the user on the zeroing in on 5 clusters
    print('The cut off is here' , Threshold) 
    print('The cut off last time was', Last_Threshold)
    print('The cut off two times back was', Threshold_2back)
    print('The number of clusters is', Clusters)
    print('The number of clusters last time was', Last_Clusters)
    print('The differential is', Differential)
    print('\n')

    #Avoid infinite loop by modifying Differential until a 5 Cluster group is found, is an issue when clusters 4-6 are similar
    if Last_Clusters == Clusters:
      Differential = Differential / 2
    if Threshold == Threshold_2back:
      Differential = Differential / 2

    #update these fields for the next round
    Last_Clusters = Clusters 
    Threshold_2back = Last_Threshold
    Last_Threshold = Threshold

  #End of clustering into groups of 5 while loop
  print('The 5 Clusters have been picked')
  print('\n')
  
  #Find the distributions of the groups and redefine
  List = np.array(ind).tolist()
  A = List.count(1)
  B = List.count(2)
  C = List.count(3)
  D = List.count(4)
  E = List.count(5)

  #How big is each cluster of profiles?, A = 1, B = 2...
  print('The original clusters were:')
  print("A =", A, "\n" + "B =", B, "\n" + "C =", C, "\n" + "D =", D, "\n" + "E =", E)
  print('\n')

  #Sort the numbers into a diction for recoding
  new_zip = zip(Counter(List).keys(), Counter(List).values())
  new_dict = dict(new_zip)
  new_dict = sorted(new_dict, key=new_dict.get, reverse=True)

  #This turns everyone's ind to an indication of rank of frequency 
  for i in range(0, len(List) - 1): 
    ind[i] = new_dict.index(List[i]) + 1

  #Find the distributions of the groups and redefine
  ind2 = np.array(ind).tolist()
  A = ind2.count(1)
  B = ind2.count(2)
  C = ind2.count(3)
  D = ind2.count(4)
  E = ind2.count(5)

  #How big is each cluster of profiles?, A = Most numerous element, B = Second most numerous element...
  print('The clusters were recoded to:')
  print("A =", A, "\n" + "B =", B, "\n" + "C =", C, "\n" + "D =", D, "\n" + "E =", E)
  print('\n')

  #Mapping the clusters 1 - 5 in the original data set
  df['Cluster'] = List
  df['Profile'] = ind

  '''
  #Set up the dendrogram / figure 
  fig, ax = plt.subplots(figsize=(25, 10)) # set size
  ax = dendrogram(linkage_matrix, orientation='top');

  #Labeling the graph
  plt.tick_params(\
      axis = 'x',          # changes apply to the x-axis
      which = 'both',      # both major and minor ticks are affected
      bottom = 'off',      # ticks along the bottom edge are off
      top = 'off',         # ticks along the top edge are off
      labelbottom = 'off')

  plt.tight_layout() #show plot with tight layout
  print('Dendrogram Made!')
  print('\n')
  '''

  df['State'] = df['Profile']
  print(df[:10])
  columns = ['YrsLic','NumVeh' ,'PriorBI' ,'YwP' ,'Source' ,'Accidents' ,'NumDriv', 'Profile']
  print('\n 1')
  hierarchical_clust_var(input_df = df[columns], var = 'Profile', linkage_matrix = linkage_matrix)
