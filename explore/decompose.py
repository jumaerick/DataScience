import streamlit as st
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
