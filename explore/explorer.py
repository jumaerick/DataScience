from commonLibraries.libraries import *

dataset = dataLoader.getData()


def distributions():
    st.markdown(
        'Select any daterange below from which you wish to base your observations')
    # st.dataframe(len(dataset['date'].value_counts()))
    # months = ("January", "February", "March", "April", "May", "June", 
    #       "July", "August", "September", "October", "November", "December")
    # days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
#     year = st.selectbox('Select Year', dataset['year'].unique())
    min_date = dataset.index.min().date()
    max_date = dataset.index.max().date()
    adder_days = pd.to_datetime('1996-01-01').date()
#     st.text(adder_days)
    Start_date = st.date_input('Start_date', min_value=min_date,
                            max_value=max_date, value=min_date)
    End_date = st.date_input('End_date', min_value=min_date,
                            max_value=max_date, value=adder_days)
#     month = st.selectbox('Select Month', months)
#     day = st.selectbox('Select Day', days)
    fig = plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='value (million $)',
                 data=dataset.loc[Start_date:End_date:, ['value (million $)']])
#     sns.boxplot(x='month', y='value (million $)', data = dataset)
    st.pyplot(plt)
    st.markdown('There is a general increase in trend in the data with some seasonal variations')
#     st.markdown('The time series for the one year interval starting from the minimum date of the observations')

    # st.title('Boxplot Analysis')
    # freq_option =  st.selectbox('Weekly or Monthly sales value boxplot', ('Weekly', 'Monthly'))
    # option = ''
    # if (freq_option.lower() == 'weekly'):
    #     option = 'day'
    # else:
    #     option = 'month'
        
    # fig = plt.figure(figsize=(12, 6))
    # sns.boxplot(x = option, y = 'value (million $)', data = dataset)
    # st.pyplot(plt)

    
