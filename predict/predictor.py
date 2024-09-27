from explore import dataLoader
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score

dataset = dataLoader.loadData()


class Clustering:
    def __init__(self, n_iters = 15, scores = {}):
        self.dataset = dataset
        self.n_iters = n_iters

    def test(self):
        return self.n_iters
    
    def scoring(self, features):
        """
        Define the model
        """
        X = self.dataset[features]
        scores = {'iters': [], 'inertia': [], 'dbs': [], 'shs': []}
        for i in range(2, self.n_iters):
            model = KMeans(n_clusters = i)
            model.fit(self.dataset[features])
            clusters = model.labels_
            scores['iters'].append(i)
            scores['inertia'].append(model.inertia_)
            scores['dbs'].append(davies_bouldin_score(X, labels = clusters))
            scores['shs'].append(silhouette_score(X, labels = clusters))
        return scores
        
    
cluster = Clustering()

def selectFeatures():
    col1, col2, col3 = st.columns(3)
    with col1:
        feature1 = st.selectbox('Feature X', ('Annual Income (k$)','Spending Score (1-100)', 'Age'))

    with col3:
        feature2 = st.selectbox('Feature y', ('Spending Score (1-100)','Annual Income (k$)', 'Age'))

    return {'feature1':feature1, 'feature2':feature2}

st.text(selectFeatures())

scores = cluster.scoring(['Annual Income (k$)','Spending Score (1-100)'])

def plotInertias():
    fig = plt.figure()
    plt.plot(scores['iters'], scores['inertia'])
    plt.xlabel('Number of iterations')
    plt.ylabel('Computed inertia')
    return st.pyplot(plt)


def plotSHS():
    fig = plt.figure()
    plt.plot(scores['iters'], scores['shs'], c='g')
    plt.xlabel('Number of iterations')
    plt.ylabel('SIilhoutte Score')
    return st.pyplot(plt)


def plotDBS():
    fig = plt.figure()
    plt.plot(scores['iters'], scores['dbs'], c='y')
    plt.xlabel('Number of iterations')
    plt.ylabel('Davies Bouldine Score')
    return st.pyplot(plt)