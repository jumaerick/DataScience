from explore import dataLoader
import streamlit as st
import matplotlib.pyplot as plt

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
    st.markdown(';Distribution of the dataset by Gender
    genderDistribution = dataset['Gender'].value_counts() / len(dataset['Gender'].value_counts())
    fig = plt.figure(figsize = (2,2))
    plt.pie(genderDistribution, labels = genderDistribution.index, autopct='%.1f%%')
    plt.title('Distribution of the dataset by Gender')
    st.pyplot(fig)
