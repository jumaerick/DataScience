import streamlit as st
from explore import explorer

def main():
    explorer.distributions()
    # st.dataframe(dataset.set_index('date'))

if __name__ == '__main__':
    main()