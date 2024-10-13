import os
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

filename = 'creditcard.csv'
path = '../datasets'

def importData():
    # df = pd.read_csv(os.path.join(path, filename), header = None)
    # with open(os.path.join(path, filename)) as openfile:
    #     lines = [line.strip().split(',') for line in openfile.readlines()]
    #     cols = [i for i in range(len(lines[0]))]
    #     datadict = [{cols[key]: float(val.strip('""')) for key, val in enumerate(line)} for line in lines]
    #     df =  pd.DataFrame(datadict)
    #     df[cols[-1]] = df[cols[-1]].astype(int)
    return 


dataset = importData()

def sampleStats():
    st.markdown("""
    This is the case of unbalanced datasets with positive class being less than 1%.
    """)
    fig =plt.figure()
    plt.pie(dataset.iloc[:,-1].value_counts().values, labels=['Yes', 'No'], autopct="%.2f%%", )
    st.pyplot(fig)


def sampleChart():
    fig =plt.figure()
    sns.histplot(dataset.iloc[:, :-1])
    st.pyplot(fig)
