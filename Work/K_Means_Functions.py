import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#To check how different values of k effect the SSE (the total distance between sampels and their assigned centroids) we will plot the SSE for different values of k.
#The SSE will decrease as k (the number of groups) increases. We want to choose a k where there is a significant improvement over previous ks
def elbow_method(input_df, k_count):
    #This list will hold our SSEs (also called distortions) for different values of k
    distortions = []
    #Check performance for k = 1 through k = 10
    for i in range(1,k_count+1):
        #Instantiate k-means object
        km = KMeans(n_clusters = i,
                                #Use k-means++ to get better initialization of centroids
                                init = 'k-means++',
                                #This will run k-means 100 times with different intitial random centroids and will choose the iteration with the lowest SSE
                                n_init = 1000,
                                max_iter = 10000,
                                #If SSE changes less than tol between iterations then we stop
                                tol = 1e-08)

        #Now use K-means on the input dataframe
        km.fit(input_df)

        #The distortion for k-means is store din the intertia attribute of the km object
        distortions.append(km.inertia_)

    #Now let's plot our results. K on the x-axis, distortions on the y-axis
    plt.plot(range(1,k_count+1), distortions, marker = 'o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()


#For k = 3,4,5 we want to append the group assignment to the original dataset then examine the silhouette plots to see how well the clusters are separating and grouping the states

def silhouette_plot(input_df, append_df, num_k):
    #cm is a color map. Used to create separate colors for each cluster in an iteration of k-means
    from matplotlib import cm
    #Scikit-learn can already calculate the silhouette coefficient for a sample
    from sklearn.metrics import silhouette_samples

    km = KMeans(n_clusters = num_k,
                            #Use k-means++ to get better initialization of centroids
                            init = 'k-means++',
                            #This will run k-means 100 times with different intitial random centroids and will choose the iteration with the lowest SSE
                            n_init = 1000,
                            max_iter = 10000,
                            #If SSE changes less than tol between iterations then we stop
                            tol = 1e-08)
    cluster = km.fit_predict(input_df)
    append_df['kmeans' + str(num_k)] = cluster

    #Now we'll create silhouette plots for each of the clusters. A silhouette coefficient of 1 for a sample is ideal while 0 is poor.

    #Get distinct labels for each k-means and the number of distinct labels
    cluster_labels = np.unique(cluster)
    n_clusters = cluster_labels.shape[0]
    silhouette_vals = silhouette_samples(input_df,
                                                            cluster,
                                                            metric = 'euclidean')

    y_ax_lower, y_ax_upper = 0, 0
    yticks = []
    #enumerate will iterate over a list giving the position and item of each element
    #Here, p is the position of the k-means label and c is the value of the label
    for p, c in enumerate(cluster_labels):
        c_silhouette_vals = silhouette_vals[cluster == c]
        c_states = append_df['State'][append_df['kmeans' + str(num_k)] == c].tolist()
        c_silhouette_vals.sort()
        y_ax_upper += len(c_silhouette_vals)
        color = cm.jet(p / n_clusters)
        plt.barh(range(y_ax_lower, y_ax_upper),
                        c_silhouette_vals,
                        height = 1.0,
                        edgecolor = 'none',
                        color = color)

        #Attach state name to each point
        for state, x in zip(c_states, c_silhouette_vals):
            plt.annotate(state,
                                xy = (x/2, y_ax_lower+c_states.index(state)),
                                xytext = (0, 0),
                                textcoords = 'offset points',
                                ha = 'center',
                                va = 'bottom')

        #yticks is where we want to put the cluster label on the y-axis
        yticks.append((y_ax_lower + y_ax_upper ) / 2)
        y_ax_lower += len(c_silhouette_vals)

    silhouette_avg = np.mean(silhouette_vals)
    #Plot the avg silhouette for all samples as a dotted line
    plt.axvline(silhouette_avg
                    ,color = "red",
                    linestyle = "--")
    plt.yticks(yticks, cluster_labels + 1)
    plt.ylabel('Cluster')
    plt.xlabel('Silhouette coefficient')
    plt.show()

