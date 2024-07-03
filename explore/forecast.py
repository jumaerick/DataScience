from commonLibraries.libraries import *

from statsmodels.tsa.seasonal import seasonal_decompose

dataset = dataLoader.getData()
# results = seasonal_decompose(dataset['value (million $)'], model='additive')
dataset.iloc[:,:1] = np.log(dataset.iloc[:,:1])
dataset = dataset.iloc[:,:1].diff(1).dropna()

def seriesComponents():
    fig = plt.figure(figsize=(10, 5))
    rolling_mean = dataset.iloc[:, :1].rolling(window=13).mean()
    rolling_std = dataset.iloc[:, :1].rolling(window=13).std()
    fig = plt.figure()
    sns.set(rc={'figure.figsize':(10,5)})
    plt.plot(dataset.iloc[:, :1], color='blue', label="Original Medical data")
    plt.plot(rolling_mean, color='red', label="Rolling Mean Patient Number")
    plt.plot(rolling_std, color='black',
             label="Rolling Standard Deviation Patient Number")
    plt.legend(loc='best')
    st.markdown('Since the mean and std change with time, the time series is non stationary')
    st.pyplot(plt)


def acfPlots():
    pass