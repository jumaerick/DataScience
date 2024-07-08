from commonLibraries.libraries import *
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf, plot_predict
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX 

dataset = dataLoader.getData()
results = seasonal_decompose(dataset['value (million $)'], model='additive')
ts = np.log(dataset.iloc[:, :1])
# st.dataframe(ts)
ts_diff = ts.diff(1).dropna()

def autoCorrelation():
    fig = plt.figure(figsize=(12, 6))
    lag_acf = plot_acf(ts_diff, lags = 30)
    st.pyplot(plt)
    lag_pacf = plot_pacf(ts_diff, lags=30)
    st.pyplot(plt)

    model = st.selectbox('Model for forecasting', ('Select model', 'ARIMA', 'SARIMA'))
    order = st.selectbox('Order of MA', range(1, 6))
    if model =='ARIMA':
        ArimaModel(order)
    elif model == 'SARIMA':
        SarimaModel(order)
    else:
        pass


# lag_acf = acf(dataset['value (million $)'], nlags=20)

def ArimaModel(order):
    st.header('ARIMA model')
    st.markdown('AR(1) since there is a spike at lag 1 and upto lag 12 again which signifies seasonality')
    st.markdown('MA(4) since there is a spike at lag 1 to 4 and again from lag 12 which signifies seasonality')
    st.markdown('Our ARIMA model will have the terms p = 4, d = 1, q=1')
    st.text("Equation (p,d,q)")
    AR = "p the lags of dependent variable used"
    MA = "q are lagged forecast errors in prediction equation"
    d =  "Number of differencing"
    # order = st.selectbox('orde of MA', range(1, 6))
    model = ARIMA(ts_diff, order=(order, 1, 1))  
    results_AR = model.fit()  
    print(results_AR.summary())
# Actual vs Fitted
    forecast_steps = 12  # Number of steps to forecast
    forecast = results_AR.predict(start=len(ts_diff)-1, end=len(ts_diff) + forecast_steps - 1, typ='levels')
    plt.figure(figsize=(12, 6))
    plt.plot(ts_diff, color='blue', label='Actual')
    plt.plot(results_AR.fittedvalues, color='red', label='Fitted')
    plt.plot(forecast, color='green', label='Forecasted')
    plt.title('Actual, Fitted, and Forecasted Values')
    plt.legend(loc='best')
    st.pyplot(plt)


def SarimaModel(order):
    st.header('SARIMA')
    st.markdown('The presence of the seasonal component imply that the SARIMA model will be the better choice')

    modelSarimax = SARIMAX(ts_diff, 
                order=(order, 1, 1),          # non-seasonal part: (p, d, q)
                seasonal_order=(1, 1, 1, 12))  # seasonal part: (P, D, Q, s)
    results_SAR = modelSarimax.fit()  
    forecast_steps = 12 
    print(results_SAR.summary())
    forecast = results_SAR.predict(start=len(ts_diff)-1, end=len(ts_diff) + forecast_steps - 1, typ='levels')

    plt.figure(figsize=(12, 6))
    plt.plot(ts_diff, color='blue', label='Actual')
    plt.plot(results_SAR.fittedvalues, color='red', label='Fitted')
    plt.plot(forecast, color='green', label='Forecasted')
    plt.title('Actual, Fitted, and Forecasted Values')
    plt.legend(loc='best')
    st.pyplot(plt)
