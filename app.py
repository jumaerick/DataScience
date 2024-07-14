import streamlit as st
from explore import explorer
from loadData import dataLoader

st.title("Customer Lifetime Value")
st.markdown("""
This is the overall worth of a customer to the business throughout the period 
            of their relationship with the business.
""")

task_type = st.selectbox('Analysis Type', ('Multivariant','Univariant'))

def main(item):
    item = item.lower()
    if item == 'multivariant':
        explorer.scatterPlots('cost', 'revenue', hue='channel')
    else:
        explorer.getSummaries()
        explorer.checkNormalDist()
        explorer.scatterPlots('cost', 'revenue', hue='channel')


if __name__=='__main__':
    main(task_type)