import streamlit as st
from explore import explorer
from loadData import dataLoader

st.title("Customer Lifetime Value")
st.markdown("""
This is the overall worth of a customer to the business throughout the period 
            of their relationship with the business.
""")

task = st.selectbox('Select task', ('Analysis','Compute ROI', 'Compute CLTV'))

def main(item):
    if item == 'Analysis':
        task_type = st.selectbox('Analysis Type', ('Univariant', 'Multivariant'))
        if task_type == 'Multivariant':
            explorer.scatterPlots('cost', 'revenue', hue='channel')
            explorer.groupedData()
            explorer.conversionbyChannel()
        else:
            explorer.getSummaries()
            explorer.checkNormalDist()
    elif item=='Compute ROI':
        explorer.roiCalculator()
        

    elif item=='Compute CLTV':
            explorer.cltvCalcultor()
    # task_type = st.selectbox('Analysis Type', ('Multivariant','Univariant'))
    # item = item.lower()

        # explorer.scatterPlots('cost', 'revenue', hue='channel')


if __name__=='__main__':
    main(task)