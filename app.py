from modules.commonModules import *
from predict import predictor
from explore import explorer


st.title('Iris Exploration and Prediction')

option = st.selectbox('Explore or Prediction Task',
                    ('', 'Explore', 'Predict'))


def main(item):
    item = item.lower()
    if item == "explore":
        #st.title('Sample data statistics')
        # st.dataframe(explorer.dataLoader())
        #explorer.getSummaries()
        st.title('Bivariant Analysis')
        explorer.getClassDistribution()
        pass
    elif item == 'predict':
        # predictor.featureSlider(item)
        featureDict = predictor.featureSlider(item)
        predictor.makePrediction(featureDict)

if __name__ == '__main__':
    main(item=option)
