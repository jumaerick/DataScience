import streamlit as st
from modules import fileReader, calculator


st.title('Target Investment Calculator')
st.markdown(
    """
    <style>
    .stNumberInput div[data-baseweb="input"] > div:first-child {
        background-color: mediumspringgreen;
    }
    
        .stSlider div[data-baseweb="slider"] > div:first-child {
        color: lightseagreen;
    }
    tr:nth-child(even){
        background-color:#f2f2f2;
        }
        
            th:nth-child(1){
       display:none;
        }
        
    th{
              background-color:#f2f2f2; 
    }
    
    .col_heading{
        color:#000;
    }
    .st-emotion-cache-uzeiqp{
        margin-top: -4em;
    }
    .st-emotion-cache-12fmjuu{
        display:none;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# dataset = fileReader.importData()

def main():
    # fileReader.sampleStats()
    # fileReader.sampleChart()
    calculator.calculate()
    # st.text(calculator.recursive())
    # st.text(calculator.recurse())

if __name__=='__main__':
    main()