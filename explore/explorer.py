from loadData import dataLoader
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

dataset = dataLoader.getData()

def distributions():
    # st.dataframe(len(dataset['date'].value_counts()))
    months = ("January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December")
    days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

    year = st.selectbox('Select Year', dataset['year'].unique())
    month = st.selectbox('Select Month', months)
    day = st.selectbox('Select Day', days)

    # st.dataframe(dataset)
    fig = plt.figure(figsize=(10, 5))
    sns.lineplot(x = 'date', y = 'value (million $)',
                data = dataset.loc['1991-01-01':'2000-01-01':, ['value (million $)']])
    st.pyplot(plt)