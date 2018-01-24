'''
Here we are going to import the dataset created in our SAS Regions directory. I'm importing the gini_mse_by_state dataset saved as a csv.

Then I'll normailze all the variables so that we can effectively cluster the variables (magnitude matters in clustering)

Finally I'll cluster the data via k-means and hierarchical clustering methods impleneted in scikit-learn
'''

#Use Pandas to import the dataset and standardize the variables
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import sys
import os

#Functions I wrote
from K_Means_Functions import elbow_method, silhouette_plot
from Hierarchical_Clustering_Functions import hierarchical_clust

#Specify our working directory and the name of the csv we want to import then read that into a Pandas dataframe
os.chdir('//chnas01/urc/URC-Private/Research/UW Models/4 Projects/2016/NBUS New Regions/4 Modeling/Clustering/')
input_file = 'gini_mse_by_state.csv'
data_by_state = pd.read_csv(input_file)

#Going to drop NM and add it to the worst performing cluster since it performs so much worse than every other state
data_by_state = data_by_state[data_by_state['State'] != 'NM']
data_by_state = data_by_state.reset_index(drop = True)


#Standardize all the variables by subtracting mean and dividing by SD of each variable. Standardizing so that each variable has the same weight in clustering
stdsc = StandardScaler()

print(StandardScaler())
#Want to scale numeric columns while retaining state names
numeric_cols = [col for col in data_by_state.columns if col != 'State']
data_by_state[numeric_cols] = data_by_state[numeric_cols].apply(lambda x: stdsc.fit_transform(x))


#Weight the percentage variables
weight = 1/2
data_by_state['Num_Pols_W'] = data_by_state['Num_Pols'] * (1/4)
data_by_state['Perc_Rural_W'] = data_by_state['Perc_Rural']*(weight)
data_by_state['Perc_Metro_W'] = data_by_state['Perc_Metro']*(weight)
data_by_state['Perc_Small_Metro_W'] = data_by_state['Perc_Small_Metro']*(weight)


#Create a list and dataframe of columns for just the columns we want to cluster on
#Tried this initially. Essentially double counting Gini since the SD are typically very low, CI_95_Upper and CI_95_Lower are very similar
#cluster_vars = [col for col in data_by_state.columns if col in ['MSE', 'Perc_Metro', 'Perc_Small_Metro', 'Perc_Rural', 'CI_95_Upper', 'CI_95_Lower']]
# cluster_vars = [col for col in data_by_state.columns if col in ['MSE', 'Perc_Rural', 'Perc_Metro', 'Perc_Small_Metro', 'GINI_Mean']]
cluster_vars = [col for col in data_by_state.columns if col in ['MSE',  'GINI_Mean', 'Perc_Rural_W', 'Perc_Metro_W', 'Perc_Small_Metro_W']]

cluster_df = data_by_state[cluster_vars]


#This function will show the SSE (aka distortion) for k-means clustering with different values of k. The lower the SSE, the better
#After reviewing the output of the elbow_method function call (the graph is saved in the project folder), the more clusters the better up to around 7 clusters.
elbow_method(input_df = cluster_df,
                        k_count = 15)

#This function will append the results of k-mean clustering with the given number of k to the append_df dataset. It will also produce a silhouette plot to see how the clustering is performing.
silhouette_plot(input_df = cluster_df,
                        append_df = data_by_state,
                        num_k=2)
silhouette_plot(input_df = cluster_df,
                        append_df = data_by_state,
                        num_k=3)
silhouette_plot(input_df = cluster_df,
                        append_df = data_by_state,
                        num_k=5)


#This function will create a dendrogram and heat map for the hierarchical clustering of the input dataframe
cluster_vars.append('State')
cluster_df = data_by_state[cluster_vars]
hierarchical_clust(input_df = cluster_df)








