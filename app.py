import streamlit as st
from explore import explorer
from explore import decompose

st.title('Time Series Analysis')
option = st.sidebar.selectbox('Select a task', ('Explore','Decompose','Stationarity Test and  Differencing', 'Forecasting'))

def main(item):
    item = item.lower()
    if item == 'explore':
        explorer.distributions()
    elif item == 'decompose':
        # decompose.autoCorrelation()
        st.markdown('Decomposing the time series to its components')
        decompose.seasonalComponentPlot()
        st.markdown('The time series exhibits seasonality since peaks and troughs occur annualy')
        st.markdown('Since there exists a seasonal component, the time series is non stationary')
        decompose.residualComponentPlot()
        st.markdown('There exists unpxplained noise/randomness in the data')
        decompose.trendComponentPlot()
        st.markdown('The time series is moving in a general upwards direction')
        st.markdown('Since there exists a trend component, the time series is non stationary')
        st.markdown("")
        st.subheader('The changing mean and variation in the data at a specific window')
        decompose.rollingMeanStd()

    elif item == 'stationarity test':
        # st.markdown('Stationarity Test')
        decompose.stationarityTest()
    else:
        pass

if __name__ == '__main__':
    main(item = option)
