from explore import dataLoader
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score
import scipy.cluster.hierarchy as shc

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
        feature_n = st.selectbox('Feature x', ('Annual Income (k$)','Spending Score (1-100)', 'Age'))

    with col3:
        feature_m = st.selectbox('Feature y', ('Spending Score (1-100)','Annual Income (k$)', 'Age'))

    return {'feature1': feature_n, 'feature2':feature_m}



def plotInertias():
    features = selectFeatures()
    global scores
    scores = cluster.scoring([features['feature1'],features['feature2']])
    fig = plt.figure()
    plt.plot(scores['iters'], scores['inertia'])
    plt.xlabel('Number of iterations')
    plt.ylabel('Computed inertia')
    return st.pyplot(plt)


def plotSHS():
    fig = plt.figure()
    plt.plot(scores['iters'], scores['shs'], c='g')
    plt.xlabel('Number of iterations')
    plt.ylabel('Silhoutte Score')
    sorted_scores = sorted(scores['shs'])
    # st.text(min(sorted_scores))
    return st.pyplot(plt)


def plotDBS():
    fig = plt.figure()
    plt.plot(scores['iters'], scores['dbs'], c='y')
    plt.xlabel('Number of iterations')
    plt.ylabel('Davies Bouldine Score')
    return st.pyplot(plt)


def plotDendogram():
    fig = plt.figure()
    dend = shc.dendrogram(shc.linkage(dataset.iloc[:, 1:], method='ward'))
    st.pyplot(fig)
