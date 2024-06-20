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
    sns.pairplot(data, diag_kind='kde', hue='species')
    st.pyplot(plt)
    # return df.describe()

def getClassDistribution(data = df):
    fig = plt.figure()
    # sns.scatterplot(x = 'sepal_length', y='petal_length',  data = data, c = pd.factorize(df['species'])[0])
    x = st.selectbox('x', ('sepal_length', 'sepal_width', 'petal_length', 'petal_width'))
    y = st.selectbox('y', ('sepal_width', 'sepal_length', 'petal_length', 'petal_width'))
    if (x or y not in ('Select feature')):
        sns.scatterplot(x = x, y = y, data = data, hue = 'species')
        plt.xlabel(x)
        plt.ylabel(y)
    st.pyplot(plt)
    st.markdown("""
The sepals measurements nicely segregate the data to 3 visible classes.
""")
   st.markdown("""
The petals measurements alone results in 1 visible cluster while the other two clusters overlap.
""")
