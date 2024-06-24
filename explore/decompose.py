from commonLibraries.libraries import *
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

dataset = dataLoader.getData()
results = seasonal_decompose(dataset['value (million $)'], model='additive')


def autoCorrelation():
    fig = plt.figure(figsize=(12, 6))
    pd.plotting.autocorrelation_plot(dataset.iloc[:, :2])
    st.pyplot(plt)


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


def stationarityTest():
    st.markdown('Performing Dicky-Fuller test')
    st.markdown('H0 is the timeseries is not stationary')
    st.markdown('H1 timeseries is stationary')
    dftest = adfuller(dataset.iloc[:, :1], autolag='AIC')
    dfoutput = pd.Series(dftest[:4], index=['Test statistics',
                                            'p-value', '#Lags used', 'Number of Observations']).T
    for key, value in dftest[4].items():
        dfoutput['Criticat value (%s)' % key] = value
    st.table(dfoutput)

    dataset.iloc[:, :1].diff()

    if dfoutput['p-value'] >= 0.05:
        st.markdown('Since the p-value > 0.05 we accept the null hypothesis')
        st.markdown('Therefore the timeseries is not stationary')
    else:
        pass


def rollingMeanStd():
    period = st.selectbox('select window period', (7, 14, 21, 30))
    rolling_mean = dataset.iloc[:, :1].rolling(window=period).mean()
    rolling_std = dataset.iloc[:, :1].rolling(window=period).std()
    fig = plt.figure(figsize=(10, 5))
    plt.plot(dataset.iloc[:, :1], color='blue', label="Original Medical data")
    plt.plot(rolling_mean, color='red', label="Rolling Mean Patient Number")
    plt.plot(rolling_std, color='black',
             label="Rolling Standard Deviation Patient Number")
    plt.legend(loc='best')
    st.pyplot(plt)
