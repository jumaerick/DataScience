import pandas as pd
import os


def getData(filename = 'medicine_sales.csv'):
    path = './datasets'
    df = pd.read_csv(os.path.join(path, filename), parse_dates = True)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['year'] = pd.DatetimeIndex(df.index).year
    df['month'] = pd.DatetimeIndex(df.index).month_name()
    df['day'] = pd.DatetimeIndex(df.index).day_name()
    return df

# dataset = getData('medicine_sales.csv')
