from modules.commonModules import *

def dataLoader():
    iris = load_iris()
    isa = [i[:-4].strip() for i in np.unique(iris.feature_names)]
    target_names = ['_'.join(i.split(' ')) for i in isa]

    df = pd.DataFrame(data = iris.data, columns = target_names)
    df['class'] = iris.target
    d_s = {0:'Virginica', 1:'Versicolor', 2:'Setosa'}
    dsw = lambda x :d_s[x]
    df['species'] = [dsw(i) for i in iris.target]
    return df

df = dataLoader()


def getSummaries(data = df):
    fig = plt.figure()
    plt.pie(data.loc[:, 'class'].value_counts(), labels = data.loc[:, 'species'].value_counts().index, autopct='%.2f%%')
    # st.dataframe(data.loc[:, 'class'].value_counts())
    # sns.pairplot(data, diag_kind='hist', hue='species')
    st.pyplot(plt)
    st.markdown('This is a balanced dataset with equal number of instances for each of the 3 classes')

def getHeatmaps(data = df):
    fig = plt.figure()
    numericFeatures = data.select_dtypes(exclude='object')
    
    corrCoeff = numericFeatures.corr(method='pearson')
    sns.heatmap(corrCoeff, cmap='inferno', annot=True)
    st.pyplot(plt)
    st.markdown('The petal width has a weak positive correlation with other features and the target classes')
    st.markdown(""" The sepal length and sepal width have a strong positive correlation with the target classes.
                They therefore seam to explain the target classes much better.
                """)

    # return df.describe()

def getClassDistribution(data = df):
    fig = plt.figure()
    # sns.scatterplot(x = 'sepal_length', y='petal_length',  data = data, c = pd.factorize(df['species'])[0])
    x = st.selectbox('Feature One', ('sepal_length', 'sepal_width', 'petal_length', 'petal_width'))
    y = st.selectbox('Feature Two', ('sepal_width', 'sepal_length', 'petal_length', 'petal_width'))
    if (x or y not in ('Select feature')):
        sns.scatterplot(x = x, y = y, data = data, hue = 'species')
        plt.xlabel(x)
        plt.ylabel(y)
    st.pyplot(plt)
    st.markdown("""
    The sepals measurements segregate the data to 3 visible clusters with a few points overlapping.
    """)
    st.markdown("""
   The petals measurements alone results in 1 distinct cluster and 2 overlapping clusters.
    """)
