from commonLibraries.libraries import *
from statsmodels.tsa.seasonal import seasonal_decompose

dataset = dataLoader.getData()
results = seasonal_decompose(dataset['value (million $)'], model='additive')

def seasonalComponentPlot():
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(results.seasonal)
    plt.title('The seasonal component of the timeseries')
    st.pyplot(plt)


def residualComponentPlot():
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(results.resid)
    plt.title('The residual component of the timeseries')
    st.pyplot(plt)

def trendComponentPlot():
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(results.trend)
    plt.title('The trend component of the timeseries')
    st.pyplot(plt)