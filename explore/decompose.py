from commonLibraries.libraries import *
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

dataset = dataLoader.getData()
results = seasonal_decompose(dataset['value (million $)'], model='additive')

def autoCorrelation():
    fig = plt.figure(figsize=(12, 6))
    pd.plotting.autocorrelation_plot(dataset.iloc[:, :2])
    st.pyplot(plt)


# def seasonalComponentPlot():
#     fig = plt.figure(figsize=(12, 6))
#     pd.plotting.autocorrelation_plot(dataset.iloc[:, :2])
#     st.pyplot(plt)


def seasonalComponentPlot():
    fig = plt.figure()
    sns.set(rc={'figure.figsize': (10, 5)})
    sns.lineplot(results.seasonal)
    plt.title('The seasonal component of the timeseries')
    st.pyplot(plt)


def residualComponentPlot():
    fig = plt.figure()
    sns.set(rc={'figure.figsize': (10, 5)})
    sns.lineplot(results.resid)
    plt.title('The residual component of the timeseries')
    st.pyplot(plt)


def trendComponentPlot():
    fig = plt.figure()
    sns.set(rc={'figure.figsize': (10, 5)})
    sns.lineplot(results.trend)
    plt.title('The trend component of the timeseries')
    st.pyplot(plt)


def stationarityTest():
    st.markdown('Performing Dicky-Fuller test')
    st.markdown('H0 is the timeseries is not stationary')
    st.markdown('H1 timeseries is stationary')
    dftest = adfuller(dataset.iloc[:, :1], autolag='AIC')


def rollingMeanStd():
    st.markdown(
        'The rolling helps us determine by how much the present value changes with past value')
    period = st.selectbox('select window period', (7, 14, 21, 30))
    rolling_mean = dataset.iloc[:, :1].rolling(window=period).mean()
    rolling_std = dataset.iloc[:, :1].rolling(window=period).std()
    fig = plt.figure()
    sns.set(rc={'figure.figsize': (10, 5)})
    plt.plot(dataset.iloc[:, :1], color='blue', label="Original Medical data")
    plt.plot(rolling_mean, color='red', label="Rolling Mean Patient Number")
    plt.plot(rolling_std, color='black',
             label="Rolling Standard Deviation Patient Number")
    plt.legend(loc='best')
    st.pyplot(plt)
    st.markdown(
        'Since the mean and std change with time, the time series is non stationary')

# def stationarityTest():
#     st.subheader('Performing Dicky-Fuller test')
#     st.markdown('H0 is the timeseries is not stationary')
#     st.markdown('H1 timeseries is stationary')
#     threshold = st.select_slider('select threshold',(np.arange(0.01, 0.12, 0.01)) )
#     dftest = adfuller(dataset.iloc[:, :1], autolag='AIC')
#     dfoutput = pd.Series(dftest[:4], index=['Test statistics',
#                                             'p-value', '#Lags used', 'Number of Observations']).T
#     for key, value in dftest[4].items():
#         dfoutput['Criticat value (%s)' % key] = value

#     if dfoutput['p-value'] >= threshold:
#         st.table(dfoutput)
#         st.markdown('Since the p-value > %.2f we accept the null hypothesis'%(threshold))
#         st.markdown('Therefore the timeseries is not stationary')

#         st.subheader('Performing differencing to make time series stationary')
#         order = st.selectbox('Order of differencing', (range(10)))
#         differencing(dataset, order, threshold)
#     else:
#         st.table(dfoutput)
#         st.markdown('Since the p-value <  %.2f we reject the null hypothesis'%(threshold))
#         st.markdown('Therefore the timeseries is now stationary')


def stationarityTest(data=dataset, order=0, threshold=0.05):
    st.subheader('Performing Dicky-Fuller test')
    st.markdown('H0 is the timeseries is not stationary')
    st.markdown('H1 timeseries is stationary')
    st.markdown("Initial test required higher order differencing so a performed a log transform on the data")
    threshold = st.select_slider('select threshold',(np.arange(0.01, 0.12, 0.01)), value=0.05 )
    order = st.selectbox('Order of differencing', (range(5)))
    if order == 0:
        pass
    else:
        #perform a log transform
        data.iloc[:,:1] = np.log(data.iloc[:,:1])
        data = data.iloc[:,:1].diff(order).dropna()
    dftest = adfuller(data.iloc[:, :1], autolag='AIC')
    dd = st.selectbox('Choose the dataset to use', ('Original', 'Transformed'))
    ts = data.iloc[:, :1]
    if dd == 'Original':
        pass
    else:
        st.markdown(
        "Earlier tests showed higher order differencing were needed to make the time series stationary")
        st.markdown('We therefore need to transform the data first.')
        transMethod = st.selectbox(
            'Transform method', ('Logarithimic', 'Square root', 'Cube root'))
        transMethod = transMethod.lower()
        if transMethod == 'logarithimic':
            ts = np.log(ts)
        elif transMethod == 'cube root':
            ts = np.cbrt(ts)
        else:
            ts = np.sqrt(ts)
    threshold = st.select_slider(
        'select threshold', (np.arange(0.01, 0.12, 0.01)), value=0.05)
    order = st.selectbox('Order of differencing', (range(5)))

    if order == 0:
        pass
    else:
        ts = ts.diff(order).dropna()
    dftest = adfuller(ts, autolag='AIC')
    dfoutput = pd.Series(dftest[:4], index=['Test statistics',
                                            'p-value', '#Lags used', 'Number of Observations']).T
    for key, value in dftest[4].items():
        dfoutput['Criticat value (%s)' % key] = value
    st.table(dfoutput)

    if dfoutput['p-value'] >= 0.05:
        st.markdown('Since the p-value > 0.05 we accept the null hypothesis')
        st.markdown('Therefore the timeseries is not stationary')
    else:
        if dd == 'Transformed':
            st.markdown(
                'Since the p-value < %.2f we reject the null hypothesis' % (threshold))
            st.markdown(
                'Therefore applying %s transform and performing differencing of order %i makes the timeseries stationary' % (transMethod, order))
        else:
            st.markdown(
            'Since the p-value < %.2f we reject the null hypothesis' % (threshold))
            st.markdown(
            'Therefore the timeseries is now stationary after performing differencing of order %i' % (order))


def rollingMeanStd():
    period = st.selectbox('select window period', (7, 14, 21, 30))
    rolling_mean = dataset.iloc[:, :1].rolling(window=period).mean()
    rolling_std = dataset.iloc[:, :1].rolling(window=period).std()
    ts_maverage = dataset.iloc[:, :1] - rolling_mean
    ts_mastd = dataset.iloc[:, :1] - rolling_std

    fig = plt.figure(figsize=(10, 5))
    plt.plot(dataset.iloc[:, :1])
    plt.plot(dataset.iloc[:, :1], color='blue', label="Original Medical data")
    plt.plot(ts_maverage, color='red', label="Rolling Mean Patient Number")
    plt.plot(ts_mastd, color='black',
             label="Rolling Standard Deviation Patient Number")
    plt.legend(loc='best')
    st.pyplot(plt)


