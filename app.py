import streamlit as st
from explore import explorer
from predict import predictor

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
st.title('Customers Segmentation')
selection = st.sidebar.selectbox('Select a task', ('Select a task', 'EDA','Prediction'), label_visibility= 'hidden')

def main(option):
    if option == 'EDA':
        analysisype = st.selectbox('Type of analysis', ('Dataset summaries', 'Bivariant'))
        if analysisype == 'Bivariant':
            # explorer.genderDistribution() 
            explorer.featureComparison()
            explorer.bucketsComparisons()
        else:
            explorer.basicInfo()
    elif option == 'Prediction':
        cluster = predictor.Clustering()
        st.text(cluster.test())
    else:
        st.markdown("""
                    In this project, we are going to explore the mall customers dataset. The dataset consist various 
                    information of customers who visit the mall and attempts to segment them into various classes.
                    The tasks will be:
                - Exploring the dataset (EDA)
                - Segment the customers
                - Build an ML algorithm and predict the cluster where the customer belongs
                - Analyse the Davies_Bouldin and Silhouette_score as metrics for choosing k values
                       
                    """)
    pass

if __name__ == '__main__':
    main(selection)
