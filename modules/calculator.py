import streamlit as st
import numpy as np
import pandas as pd

def calculate():
    
    initial = st.number_input('Initial Investment', value = 300.00)
    target = st.number_input('Target Investment')
    profit = st.select_slider('Profit Margin', options=[round(i, 2) for i in np.arange(0.6, 0.71, 0.01)], value= 0.62)
    period = 1
    
    # initial=0.0
    if (initial > 0.0):
        #volume = st.select_slider('Trading percentage', options=[i for i in np.arange(0.0, 1.1, 0.1)], value= round((1/121*100),1))/100
        volume = st.number_input('Volume', min_value=0.0, max_value=initial,  value = initial/121)
        stages = st.select_slider('Select Stages', options=[i for i in range(1, 6, 1)], value=1)
        status = {'target': [], 'days': []}
        if(volume <= initial/121):
            while initial < target:
                stagesMultipliers = {'1': {'multiplier':1, 'formular':0},
                    '2': {'multiplier':3, 'formular': -(volume)}, 
                    '3':{'multiplier':9, 'formular': -(volume + 3**volume)},
                    '4':{'multiplier':27, 'formular': -(volume + 3*(volume) + 9*(volume)) },
                    '5':{'multiplier':81, 'formular': -(volume + 3*(volume) + 9*(volume) + 27*(volume))},
                    }
                stageStr = str(stages)
                initial += stagesMultipliers[stageStr]['multiplier']*((volume) * profit) + stagesMultipliers[stageStr]['formular']
                # print(initial)
                period += 1
                status['target'].append(initial)
                status['days'].append(period//2)
        else : 
            stagesMultipliers = {'1': {'multiplier':1, 'formular':0},
                '2': {'multiplier':3, 'formular': -(volume)}, 
                '3':{'multiplier':9, 'formular': -(volume + 3**volume)},
                '4':{'multiplier':27, 'formular': -(volume + 3*(volume) + 9*(volume)) },
                '5':{'multiplier':81, 'formular': -(volume + 3*(volume) + 9*(volume) + 27*(volume))},
                }
            stageStr = str(stages)
            st.text(stagesMultipliers[stageStr]['multiplier']*((volume) * profit) + stagesMultipliers[stageStr]['formular'])
    updatedDF = pd.DataFrame()
        
    df = pd.DataFrame(status)
    days_list = []
    target_list = []
    for day in df['days'].unique():
        u_days = df[df['days'] == day].iloc[-1:,:]
        target_list.append(u_days['target'].values[0])
        days_list.append(u_days['days'].values[0])

    updatedDF['Day'] = days_list
    updatedDF['Amount'] = target_list
    
    if(len(target_list) > 1):
        
        st.write("Your investment will amount to **%.2f** USDT in **%d** days."%(target_list[-1], days_list[-1]))
        
        st.subheader('Detailed daily earnings breakdown')
        
        # st.table(updatedDF, hide_index=True, use_container_width=True)
        st.table(updatedDF)
    
    pass


def recursive(nums = [2,5,8,9]):
    summer= 0
    if len(nums)<1:
        return summer
    
    elif len(nums) ==1:
        return summer + nums[0]
    else:
        return summer+nums[0]+recursive(nums[1:])
    
    
def recurse(options = [i for i in range(1, 6, 1)]):
    initial =400
    volume = 1/121
    profit = 0.62
    for option in options:
        if option==1:
            # initial += ((initial*volume) * profit)
            # print(initial)
            pass
        elif option==3:
            formula = 'option_'+'volume'
            # formula = (option*((initial*volume) * profit)) - (initial*volume)- 3*(initial*volume) - 9*(initial*volume)- 27*(initial*volume)
            # initial += (option*((initial*volume) * profit)) - (initial*volume)- 3*(initial*volume) - 9*(initial*volume)- 27*(initial*volume)
            stagesMultipliers = {'1': {'multiplier':1, 'formular':(option*((initial*volume) * profit))},
                                 '2': {'multiplier':3, 'formular':(option*((initial*volume) * profit)) - (initial*volume)}, 
                                 '3':{'multiplier':9, 'formular':(option*((initial*volume) * profit)) - (initial*volume) - 3*(initial*volume)},
                                 '4':{'multiplier':27, 'formular':(option*((initial*volume) * profit)) - (initial*volume) - 3*(initial*volume) - 9*(initial*volume) },
                                 '5':{'multiplier':81, 'formular':(option*((initial*volume) * profit)) - (initial*volume) - 3*(initial*volume) - 9*(initial*volume) - 27*(initial*volume)},
                                 }
            print(stagesMultipliers['2'])
            return 
        
    
