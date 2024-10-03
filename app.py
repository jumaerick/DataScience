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
selection = st.sidebar.selectbox(
    'Select a task', ('Select a task', 'EDA', 'Prediction'), label_visibility='hidden')


def main(option):
    if option == 'EDA':
        analysisype = st.selectbox(
            'Type of analysis', ('Dataset summaries', 'Bivariant'))
        if analysisype == 'Bivariant':
            # explorer.genderDistribution()
            explorer.featureComparison()
            st.markdown("""
                - Annual income and spending score plot reveals the following groups:
                    - Low income  with low spending score
                    - Low income  with high spending score
                    - Medium income  with medium spending score
                    - High income  with low spending score
                    - High income  with high spending score
                - Annual income and age plot reveals the following groups:
                    - In general, the audience under 30 years and those over 50 years have low and average annual income i.e under 80k.
                    - Audience between 30 and 50 years are spread out from low, medium to high annual income.
                - Spending score and age plot imply some loose groupings about 3, this is the same for annual income and age plot.
                
            """)

            explorer.bucketsComparisons()
            st.markdown("""
                -  Majority of the audience were below  30yrs of age.
                -  Females formed the majority of most agebrackets with males comprising of audience in their fifties and above only.    
                -  In general, were the mojority in all the spending score groups.
                -  Majority of the audience were under the medium spending score group.
                -  Majority of the audience fell under the group of medium income earners.    
                -  High income earners were equally distributed among males and females.               
                       """)
        else:

            explorer.boxPlots()
            st.markdown("""
                -  The graph is left skewed if most points (tails off) to the left mean<median<mode;
                -  The graph is right skewed if most points (tails off) to the right mean>median>mode;
                -  (Q2 - Q1) > (Q3 - Q2) left skewed.
                -  (Q2 - Q1) < (Q3 - Q2) righ skewed
                                    
            """)
            explorer.pairPlots()

            explorer.basicInfo()


    elif option == 'Prediction':
        # predictor.selectFeatures()
        st.subheader('Plot of iterations against inertia')
        predictor.plotInertias()
        st.subheader('Plot of iterations against Silhoutte Score')
        predictor.plotSHS()
        st.markdown("""
        - A higher Silhoutte Score index is well matched to its own cluster and poorly matched to the neighbouring clusters.
            """)
        st.subheader('Plot of iterations against Davies-Bouldine Score')
        predictor.plotDBS()
        st.markdown("""
        - A lower Davies - Bouldine index indicates better clustering
                    """)
        
        predictor.plotDendogram()
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
