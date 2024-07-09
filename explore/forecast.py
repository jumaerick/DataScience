from commonLibraries.libraries import *

dataset = dataLoader.getData()
results = seasonal_decompose(dataset['value (million $)'], model='additive')
ts = np.log(dataset.iloc[:, :1])
ts_diff = ts.diff(1).dropna()

def autoCorrelation():
    fig = plt.figure(figsize=(12, 6))
    st.markdown('ACF plot shows the degree of similarity between a time series and a lagged version of itself')
    st.markdown('Here we used a lags of 30 observations for the analysis')
    lag_acf = plot_acf(ts_diff, lags = 30)
    st.pyplot(plt)
    
    st.markdown('PACF plot shows the degree of similarity between a time series and a lagged version of itself after removing intermediate observation')
    lag_pacf = plot_pacf(ts_diff, lags=30)
    plt.xlabel('Lags')
    st.pyplot(plt)
    st.subheader('Inferences from the plots')
    st.markdown(
    """
    - The autocorrelations are larger for lags which are multiples of the seasonal frequency than for other lags.
        This implies the presence of seasonal component after every 12 months
    - The ACF plot suggests lag 1 is the most significant and other significant observation occur after lag 12, 24 ...
    - The partial correlations for lags 1 to 4 are statistically significant
    - The ACF suggests fitting a first order MA model
    - The PACF suggests fitting either third or fourth order AR model
    """
    )

    st.subheader('Forecasting the data for the next 24 months')
    model = st.selectbox('Model for forecasting', ('Select model', 'ARIMA', 'SARIMA'))
    if model =='ARIMA':
        ArimaModel()
    elif model == 'SARIMA':
        SarimaModel()
    else:
        pass


def ArimaModel():
    st.subheader('ARIMA model')
    st.markdown("From the ACF and PACF plots, we have MA(1)  and AR(4) or AR(3) models")
    st.markdown('Our ARIMA model will have the terms p = 3 or 4, d = 1, q=1 ')
    AR = "p the lags of dependent variable used"
    MA = "q are lagged forecast errors in prediction equation"
    d =  "Number of differencing"
    AR_order = st.selectbox('Order of AR', range(1, 6), index = range(1, 6).index(3))
    model = ARIMA(ts_diff, order=(AR_order, 1, 1))  
    results_AR = model.fit()  
    print(results_AR.summary())
# Actual vs Fitted
    forecast_steps = 24  # Number of steps to forecast
    forecast = results_AR.predict(start=len(ts_diff)-1, end=len(ts_diff) + forecast_steps - 1, typ='levels')
    plt.figure(figsize=(12, 6))
    plt.plot(ts_diff, color='blue', label='Actual')
    plt.plot(results_AR.fittedvalues, color='red', label='Fitted')
    plt.plot(forecast, color='green', label='Forecasted')
    plt.title('Actual, Fitted, and Forecasted Values')
    plt.legend(loc='best')
    st.pyplot(plt)


def SarimaModel():
    st.subheader('SARIMA model')
    st.markdown('The presence of the seasonal component imply that the SARIMA model will be the better choice compared to ARIMA.')
    MA_order = st.selectbox('Order of MA', range(1, 6), index = range(1, 6).index(3))
    modelSarimax = SARIMAX(ts_diff, 
                order=(MA_order, 1, 1),          # non-seasonal part: (p, d, q)
                seasonal_order=(1, 1, 1, 12))  # seasonal part: (P, D, Q, s)
    results_SAR = modelSarimax.fit()  
    forecast_steps = 24 
    print(results_SAR.summary())
    forecast = results_SAR.predict(start=len(ts_diff)-1, end=len(ts_diff) + forecast_steps - 1, typ='levels')

    plt.figure(figsize=(12, 6))
    plt.plot(ts_diff, color='blue', label='Actual')
    plt.plot(results_SAR.fittedvalues, color='red', label='Fitted')
    plt.plot(forecast, color='green', label='Forecasted')
    plt.title('Actual, Fitted, and Forecasted Values')
    plt.legend(loc='best')
    st.pyplot(plt)
    st.markdown("""
    From the above plots, we observe that an AR(3) or AR(4) fit the data nicely with the seasonal variations well accounted for 
                compared to ARIMA model.
    """)
