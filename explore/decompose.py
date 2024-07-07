import streamlit as st
from commonLibraries.libraries import *
from statsmodels.tsa.seasonal
from explore import explorer
from explore import decompose
from explore import forecast

st.title('Time Series Analysis')
option = st.sidebar.selectbox('Select a task', ('Explore','Stationarity Test and Differencing', 'Forecasting'))

def main(item):
    item = item.lower()
    if item == 'explore':
        explorer.distributions()
        st.subheader('Decomposing the time series to its components')
        decompose.seasonalComponentPlot()
        st.markdown('The time series exhibits seasonality since peaks and troughs occur annualy')
        decompose.residualComponentPlot()
        st.markdown('There exists unpxplained noise/randomness in the data')
        decompose.trendComponentPlot()
        st.markdown('The time series is moving in an upwards general direction')
        st.markdown("")
        st.markdown('The rolling mean and standard deviation at a window ')
        decompose.rollingMeanStd()
    # elif item == 'decompose':
    #     # decompose.autoCorrelation()
    #     st.markdown('Decomposing the time series to its components')
    #     decompose.seasonalComponentPlot()
    #     st.markdown('The time series exhibits seasonality since peaks and troughs occur annualy')
    #     decompose.residualComponentPlot()
    #     st.markdown('There exists unpxplained noise/randomness in the data')
    #     decompose.trendComponentPlot()
    #     st.markdown('The time series is moving in an upwards general direction')
    #     st.markdown("")
        # st.markdown('The rolling mean and standard deviation at a window ')
        # decompose.rollingMeanStd()

    elif item == 'stationarity test':
        # st.markdown('Stationarity Test')
        st.markdown('Since there exists a seasonal component, the time series is non stationary')
        decompose.residualComponentPlot()
        st.markdown('There exists unpxplained noise/randomness in the data')
        decompose.trendComponentPlot()
        st.markdown('The time series is moving in a general upwards direction')
        st.markdown('Since there exists a trend component, the time series is non stationary')
        st.markdown("")

# def autoCorrelation():
#     fig = plt.figure(figsize=(12, 6))
#     pd.plotting.autocorrelation_plot(dataset.iloc[:, :2])
#     st.pyplot(plt)


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

    elif item == 'stationarity test and differencing':
        st.subheader('The changing mean and variation in the data at a specific window')
        decompose.rollingMeanStd()
        st.markdown('The rolling mean and std change with time but the varion in std is slight. This implies that the time series is non stationary')
        decompose.stationarityTest()
    else:
        st.text('ARIMA Auto Regressive Intergrated Moving Average')
        #equation (p,d,q)
        #AR = p the lags of dependent variable used
        #MA = q are lagged forecast errors in prediction equation
        #d Number of differencing

        st.text('ACF')
        forecast.autoCorrelation()
        #collereation of TS with a lagged version of itself
        st.text('PACF')
        #collereation of TS with a lagged version of itself after removing variations explained by intermidiate terms 
        pass

if __name__ == '__main__':
    main(item = option)
