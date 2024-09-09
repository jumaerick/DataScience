from explore import dataLoader
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score

dataset = dataLoader.loadData()


class Clustering:
    def __init__(self, n_iters = 10):
        self.dataset = dataset
        self.n_iters = n_iters

    def test(self):
        return self.n_iters
    
    def scoring(self, features):
        """
        Define the model
        """
        X = self.dataset[features]
        scores = {'iter': [], 'inertia': [], 'dbs': [], 'shs': []}
        for i in range(2, self.n_iters):
            model = KMeans(n_clusters = i)
            model.fit(self.dataset[features])
            clusters = model.labels_
            scores['iter'].append(i)
            scores['inertia'].append(model.inertia_)
            scores['dbs'].append(davies_bouldin_score(X, labels = clusters))
            scores['shs'].append(silhouette_score(X, labels = clusters))
        fig = plt.figure()
        plt.plot( scores['iter'], scores['shs'])
        plt.plot( scores['iter'], scores['dbs'])
        return st.pyplot(plt)
        
    
cluster = Clustering()

def performClustering():
    return cluster.scoring(['Age','Spending Score (1-100)'])