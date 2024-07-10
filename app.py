import streamlit as st
from explore import explorer
from explore import decompose
from explore import forecast

st.sidebar.title('Time Series Analysis')
option = st.sidebar.selectbox('Select a task', ('Explore','Stationarity test and differencing', 'Forecasting'))

def main(item):
    item = item.lower()
    if item == 'explore':
        st.subheader('Medicine sales data and Value in millions')
        explorer.distributions()
        st.subheader('Decomposing the time series to its components')
        decompose.trendComponentPlot()
        decompose.seasonalComponentPlot()
        decompose.residualComponentPlot()



    elif item == 'stationarity test and differencing':
        st.subheader('The rolling mean and std in the data at a specific window')
        decompose.rollingMeanStd()
        decompose.stationarityTest()

    else:
        st.subheader('ACF and PACF plots')
        forecast.autoCorrelation()

if __name__ == '__main__':
    main(item = option)
