import streamlit as st
from explore import explorer
from explore import decompose

st.title('Time Series Analysis')
option = st.sidebar.selectbox('Select a task', ('Explore','Decompose','Stationarity Test', 'Forecasting'))

def main(item):
    item = item.lower()
    if item == 'explore':
        explorer.distributions()
    elif item == 'decompose':
        # decompose.autoCorrelation()
        st.markdown('Decomposing the time series to its components')
        decompose.seasonalComponentPlot()
        st.markdown('The time series exhibits seasonality since peaks and troughs occur annualy')
        decompose.residualComponentPlot()
        st.markdown('There exists unpxplained noise/randomness in the data')
        decompose.trendComponentPlot()
        st.markdown('The time series is moving in an upwards general direction')
        st.markdown("")
        st.markdown('The rolling mean and standard deviation at a window ')
        decompose.rollingMeanStd()

    elif item == 'stationarity test':
        # st.markdown('Stationarity Test')
        decompose.stationarityTest()
    else:
        pass

if __name__ == '__main__':
    main(item = option)
