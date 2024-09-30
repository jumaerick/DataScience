from explore import dataLoader
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

dataset = dataLoader.loadData()

def basicInfo():
    """
    Inspecting various information about the dataset
    """
    st.markdown("\n ### Verifying the data types of various features \n")
    st.text(dataset.dtypes)
    st.markdown("\n ### Checking the count of unique entries for each feature \n")
    st.text(dataset.nunique())
    st.markdown("\n ### Checking the count of null entries for each feature \n")
    st.text(dataset.isnull().sum())
    st.markdown("\n ### Checking the basic statistical information of each feature \n")
    st.table(dataset.describe())
    
def genderDistribution():
    """
    Distribution of the dataset by Gender
    """
    st.markdown('Distribution of the dataset by Gender')
    genderDistribution = dataset['Gender'].value_counts() / len(dataset['Gender'].value_counts())
    fig = plt.figure(figsize = (2,2))
    plt.pie(genderDistribution, labels = genderDistribution.index, autopct='%.1f%%')
    # plt.title('Distribution of the dataset by Gender')
    st.pyplot(fig)

def pairDistribution():
    fig = plt.figure(figsize=(10, 5))
    # sns.boxplot(dataset, orient='h')
    sns.pairplot(dataset, hue='Age')
    st.pyplot(fig)


def featureComparison():
    plt.figure(figsize=(10,5))

    col1, col2, col3 = st.columns(3)
    with col1:
        feature1 = st.selectbox('Feature X', ('Annual Income (k$)','Spending Score (1-100)', 'Age'))

    with col3:
        feature2 = st.selectbox('Feature y', ('Spending Score (1-100)','Annual Income (k$)', 'Age'))

    fig = plt.figure(figsize = (10, 8))
    sns.scatterplot(x = feature1, y = feature2, data = dataset)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.title(f'Plot of {feature1} vs {feature2}')
    st.pyplot(fig)


def bucketsComparisons():
    """
    Since these are continous data, we are going to split them into buckets and see the distributions by Gender info
    """
    st.subheader("Splitting continous features into buckets and visualize the distributions by Gender.")
    feature = st.selectbox('Feature', ('Spending Score (1-100)','Annual Income (k$)', 'Age'))

    if feature == 'Age':
        bins, labels = [18, 30, 40, 50, 70], ['AudienceInTwenties','AudienceInThirties','AudienceInForties','AudienceInFifties']

    elif feature == 'Annual Income (k$)':
        bins, labels = [15, 50, 80, 137], ['LowIncomeEarners','MediumIncomeEarners','HighIncomeEarners']

    elif feature == 'Spending Score (1-100)':
        bins, labels = [1, 40, 70, 100], ['LowSpendingScore','MediumSpendingScore','HighSpendingScore']

    features = pd.cut(dataset[feature], bins = bins, labels = labels)
    fig = plt.figure(figsize=(10,6))
    plt.title(f'{feature} Composition by gender')
    sns.countplot(x = features, hue='Gender', data = dataset)
    st.pyplot(fig)
