import streamlit as st
from explore import explorer
from explore import decompose

st.title('Time Series Analysis')
option = st.sidebar.selectbox('Select a task', ('explore','decompose','forecast'))

def main(item):
    if item == 'explore':
        explorer.distributions()
    elif item == 'decompose':
        st.markdown('Decomposing the time series to its components')
        decompose.seasonalComponentPlot()
        decompose.residualComponentPlot()
        decompose.trendComponentPlot()
    else:
        pass

    # st.dataframe(dataset.set_index('date'))

if __name__ == '__main__':
    main(item = option)