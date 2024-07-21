import streamlit as st
from explore import explorer
from loadData import dataLoader

st.title("Customer Lifetime Value")

st.markdown(
    """
    <style>
    .stSelectbox div[data-baseweb="select"] > div:first-child {
        background-color: mediumspringgreen;
    }
    </style>
    """,
    unsafe_allow_html=True
)

task = st.selectbox('Select task', ('Analysis','Compute ROI', 'Compute CLTV'))

def main(item):
    if item == 'Analysis':
        # task_type = st.selectbox('Analysis Type', ('Univariant', 'Multivariant'))
        # if task_type == 'Multivariant':
            st.subheader("Feature summaries and distribution types")
            explorer.getSummaries()
            explorer.checkNormalDist()
            st.subheader('Bivariant Analysis')
            explorer.scatterPlots('cost', 'revenue', hue='channel')
            explorer.groupedData()
            explorer.conversionbyChannel()

    elif item=='Compute ROI':
        explorer.roiCalculator()
        

    elif item=='Compute CLTV':
            explorer.cltvCalcultor()
    # task_type = st.selectbox('Analysis Type', ('Multivariant','Univariant'))
    # item = item.lower()

        # explorer.scatterPlots('cost', 'revenue', hue='channel')


if __name__=='__main__':
    main(task)


