import pandas as pd
import streamlit as st
import os


"""
Read the file to a list of dictionaries
"""
path = '.'
def loadData(filename = 'Mall_customers.csv'):
    file = pd.read_csv('transactions.csv')
    with open(file) as openFile:
        lines = [line.strip().split(',') for line in openFile.readlines()]
        cols =  lines[0]
        data = [{cols[key]:val for key, val in enumerate(line)} for line in lines[1:]]
    df = pd.DataFrame(data)
    # df.columns.tolist().remove(df.columns[df.columns.tolist().index('Gender')])
    cols =   df.columns.tolist()
    cols.remove('Gender')
    for col in cols:
        df[col] = df[col].astype(float)
    # df = [df[col].astype(float) for col in cols]
    # st.text(df)
    df = pd.read_csv('Mall_Customers.csv')
    return df.iloc[:, 1:]


dataset = pd.read_csv('Mall_Customers.csv')