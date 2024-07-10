from commonLibraries.libraries import *

dataset = dataLoader.getData()
results = seasonal_decompose(dataset['value (million $)'], model='additive')

def seasonalComponentPlot():
    fig = plt.figure()
    sns.set(rc={'figure.figsize': (10, 5)})
    sns.lineplot(results.seasonal)
    plt.title('The seasonal component of the timeseries')
    st.pyplot(plt)
    st.markdown('The time series exhibits seasonality since peaks and troughs occur annualy')


def residualComponentPlot():
    fig = plt.figure()
    sns.set(rc={'figure.figsize': (10, 5)})
    sns.lineplot(results.resid)
    plt.title('The residual component of the timeseries')
    st.pyplot(plt)
    st.markdown('There exists unpxplained noise/randomness in the data')


def trendComponentPlot():
    fig = plt.figure()
    sns.set(rc={'figure.figsize': (10, 5)})
    sns.lineplot(results.trend)
    plt.title('The trend component of the timeseries')
    st.pyplot(plt)
    st.markdown('The time series is moving in an upwards general direction')


def stationarityTest():
    st.markdown('Performing ADF test for stationarity')
    st.markdown('H0 is the timeseries is not stationary')
    st.markdown('H1 timeseries is stationary')
    dftest = adfuller(dataset.iloc[:, :1], autolag='AIC')


def rollingMeanStd():
    st.markdown(
        'The rolling mean and std help us determine by how much the present value changes with past value')
    period = st.selectbox('Select window period', (7, 14, 21, 30))
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
    st.markdown('The rolling mean and std change with time but the variation in std is slight. This implies that the time series is non stationary')


def stationarityTest(data=dataset, order=0, threshold=0.05):
    st.subheader('Performing Dicky-Fuller test')
    st.markdown('The null hypothesis H0  - The timeseries is not stationary')
    st.markdown('The alternative hypothesis H1 - The timeseries is stationary')

    dftest = adfuller(data.iloc[:, :1], autolag='AIC')
    dd = st.selectbox('Choose the dataset to perform the test on', ('Select dataset', 'Original', 'Transformed'))
    adFullerTest(dd)


def adFullerTest(dd):
    ts = dataset.iloc[:, :1]
    if dd not in ('Original', 'Transformed'):
        pass
    elif dd == 'Original':
        adfResults(dd, ts)
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

        adfResults(dd, ts, transMethod)

def adfResults(dd, ts, transMethod=None):
    threshold = st.select_slider(
    'Select threshold', (np.arange(0.01, 0.12, 0.01)), value=0.05)
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
    pass



