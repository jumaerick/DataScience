import streamlit as st
from explore import explorer

st.title('Time Series Analysis')
option = st.sidebar.selectbox('Select a task', ('explore','decompose','forecast'))

def main(item):
    explorer.distributions()
    # st.dataframe(dataset.set_index('date'))

if __name__ == '__main__':
    main(item = option)