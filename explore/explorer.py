from commonLibraries.libraries import *
from loadData import dataLoader

dataset = dataLoader.readFile()

def getSummaries():
    st.table(dataset.describe())

def checkNormalDist():
    st.text("Check if the features follow normal distribution")
    sns.pairplot(dataset, diag_kind='kde')
    st.pyplot(plt)
    st.markdown("""
    - The wide top for revenue curve imply wide variations in the datasets. This explains the large standard deviations 
                for revenue in the data summaries.
    - The curves for the costs imply possibility of two classes.
    - The curves for the conversion_rate imply possibility of three  overlapping classes.
    """)
    

def scatterPlots(feature_x, feature_y, hue=None):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Feature x")
        feature_x = st.selectbox('X', ('Cost', 'Revenue', 'Conversion_Rate'), label_visibility = 'hidden')

    with col3:
        st.subheader("Feature y")
        feature_y = st.selectbox('y', ('Revenue', 'Cost','Conversion_Rate'), label_visibility = 'hidden')

    feature_x = feature_x.lower()
    feature_y= feature_y.lower()

    st.markdown(f"A plot of variation of {feature_x} and {feature_y}")
    plt.figure(figsize=(8,6))
    sns.scatterplot(x = feature_x, y = feature_y , hue = hue, data = dataset)
    st.pyplot(plt)
    
   

