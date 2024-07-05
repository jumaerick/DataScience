from commonLibraries.libraries import *
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf, plot_predict
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import sarimax

dataset = dataLoader.getData()
results = seasonal_decompose(dataset['value (million $)'], model='additive')

def autoCorrelation():
    fig = plt.figure(figsize=(12, 6))
    ts = np.log(dataset.iloc[:, :1])
    # st.dataframe(ts)
    ts_diff = ts.diff(1).dropna()
    lag_acf = plot_acf(ts_diff, lags = 30)
    # pd.plotting.autocorrelation_plot(dataset.iloc[:12, :1])
    st.pyplot(plt)

    lag_pacf = plot_pacf(ts_diff, lags=30)
    st.pyplot(plt)
    st.header('ARIMA model')
    st.markdown('AR(1) since there is a spike at lag 1 and upto lag 12 again which signifies seasonality')
    st.markdown('MA(4) since there is a spike at lag 1 to 4 and again from lag 12 which signifies seasonality')
    st.markdown('Our ARIMA model will have the terms p = 4, d = 1, q=1')
    model = ARIMA(ts_diff, order=(4, 1, 1))  
    results_AR = model.fit()  
    # st.text(results_AR.summary())
# Actual vs Fitted
    forecast_steps = 12  # Number of steps to forecast
    forecast = results_AR.predict(start=len(ts_diff)-forecast_steps, end=len(ts_diff) + forecast_steps - 1, typ='levels')
    # Convert forecasted values to a pandas Series with appropriate index
    # forecast_index = pd.date_range(start=ts_diff.index[-1], periods=forecast_steps + 1, freq='M')[1:]

    # forecast_series = pd.DataFrame(forecast, index=forecast_index.date)
    st.text(forecast)

    # Print or display the forecasted values
    # print("Forecasted Values:")
    # print(forecast_series)
    # plt.plot(valid, label='Valid')
    plt.figure(figsize=(12, 6))
    plt.plot(ts_diff, color='blue', label='Actual')
    plt.plot(results_AR.fittedvalues, color='red', label='Fitted')
    plt.plot(forecast, color='green', label='Forecasted')
    plt.title('Actual, Fitted, and Forecasted Values')
    # st.dataframe(forecast_series)
    # plt.plot(test_forecast, color='green')

    plt.legend(loc='best')
    st.pyplot(plt)

    st.header('SARIMA')
    st.markdown('The presence of the seasonal component imply that the SARIMA model will be the better choice')



# lag_acf = acf(dataset['value (million $)'], nlags=20)
