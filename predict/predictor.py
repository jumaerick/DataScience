from modules.commonModules import *
import tensorflow as tf
from keras.models import load_model
from keras.saving import register_keras_serializable
from keras.models import Sequential
import keras


def get_data():
    iris = load_iris()
    isa = [i[:-4].strip() for i in np.unique(iris.feature_names)]
    target_names = ['_'.join(i.split(' ')) for i in isa]

    df = pd.DataFrame(data=iris.data, columns=target_names)
    df['class'] = iris.target
    d_s = {0: 'Virginica', 1: 'Versicolor', 2: 'Setosa'}
    def dsw(x): return d_s[x]
    df['species'] = [dsw(i) for i in df['class']]
    return df


def getIrisRaw():
    iris = load_iris()
    return iris


df = get_data()


@st.cache_data
def get_scaler():
    # Clean data
    X = df.iloc[:, :4]
    y = np.zeros(shape=(X.shape[0], 3))

    for i, val in enumerate(df['class']):
        if val == 'Virginica':
            y[i, :] = np.array([1, 0, 0])
        elif val == 'Versicolor':
            y[i, :] = np.array([0, 1, 0])
        elif val == 'Setosa':
            y[i, :] = np.array([0, 0, 1])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=100)

    # Scale data
    scaler = StandardScaler()
    scaler.fit_transform(X_train)
    return scaler


scaler = get_scaler()


def featureSlider(item):
    st.sidebar.header('Input Features')
    sepal_length = st.sidebar.slider(
        label='Sepal Length',
        min_value=0.0,
        max_value=df['sepal_length'].max(),
        value=round(df['sepal_length'].min(), 1),
        step=0.1)
    sepal_width = st.sidebar.slider(
        label='Sepal Width',
        min_value=0.0,
        max_value=df['sepal_width'].max(),
        value=round(df['sepal_width'].min(), 1),
        step=0.1)
    petal_length = st.sidebar.slider(
        label='Petal Length',
        min_value=0.0,
        max_value=df['petal_length'].max(),
        value=round(df['petal_length'].min(), 1),
        step=0.1)
    petal_width = st.sidebar.slider(
        label='Petal Width',
        min_value=0.0,
        max_value=df['petal_width'].max(),
        value=round(df['petal_width'].min(), 1),
        step=0.1)
    X_a = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    X_scaled = scaler.transform(X_a)
    return X_scaled


# @register_keras_serializable()
# class IrisModel(keras.Model):
#     def __init__(self):
#         super(IrisModel, self).__init__()
#         self.flattenLayer = keras.layers.Flatten()
#         self.denseOne = keras.layers.Dense(units = 20, activation='relu')
#         self.denseTwo = keras.layers.Dense(3, activation = 'softmax')

#     # @tf.function
#     def call(self, x):
#         x = self.flattenLayer(x)
#         x = self.denseOne(x)
#         x = self.denseTwo(x)
#         return x


class DataLoader:
    def __init__(self):
        self.data = getIrisRaw().data
        self.target = getIrisRaw().target

    def splitData(self):
        (train_data, test_data, train_labels, test_labels) = train_test_split(
            self.data, self.target, test_size=0.2, random_state=0)
        return {'train_data': train_data, 'test_data': test_data, 'train_labels': train_labels, 'test_labels': test_labels}


def trainModel():

    dataLoader = DataLoader()
    loadedData = dataLoader.splitData()

    model = Sequential()
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(units=20, activation='relu'))
    model.add(keras.layers.Dense(3, activation='softmax'))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(loadedData['train_data'], loadedData['train_labels'], batch_size=10, epochs=50,
              validation_data=[loadedData['test_data'], loadedData['test_labels']], validation_batch_size=5)

    print(f"Test Accuracy: %.2f" % (model.evaluate(
        loadedData['test_data'], loadedData['test_labels']))[-1])
    print(f"Train Accuracy: %.2f" % (model.evaluate(
        loadedData['train_data'], loadedData['train_labels']))[-1])
    model.save("./mlModels/model.keras")
    pass


# model = load_model('./mlModels/model.keras', custom_objects={'IrisModel': IrisModel})
model = load_model('./mlModels/model.keras')
# Make predictions
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy', metrics=['accuracy'])


def makePrediction(payload):
    y_pred = model.predict(payload)
    df_pred = pd.DataFrame({
        'Species': ['Virginica', 'Versicolor', 'Setosa'],
        'Confidence': y_pred.flatten()
    })
    # st.dataframe(df_pred)
    fig = plt.figure()
    sns.barplot(x='Species', y='Confidence', data=df_pred, hue='Species')
    st.pyplot(plt)
