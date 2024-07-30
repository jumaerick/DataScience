import streamlit as st
from modules import fileReader

st.title('heeloo')

dataset = fileReader.importData()

def main():
    fileReader.sampleStats()
    fileReader.sampleChart()

if __name__=='__main__':
    main()