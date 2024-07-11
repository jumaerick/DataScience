from modules.commonModules import *
from predict import predictor
from explore import explorer


st.title('Iris Exploration and Prediction')

option = st.selectbox('Explore or Prediction Task',
                    ('Select Task', 'Explore', 'Predict'))


def main(item):
    item = item.lower()
    if item == "explore":
        analysisType = st.selectbox('Analysis Type', ('Univariant', 'Bivariant'))
        analysisType = analysisType.lower()
        if analysisType == 'univariant':
            st.subheader('Univariant Analysis')
            explorer.getSummaries()
        elif analysisType == 'bivariant':
            st.subheader('Bivariant Analysis')
            explorer.getClassDistribution()
            explorer.getHeatmaps()

    elif item == 'predict':
        # predictor.featureSlider(item)
        st.subheader('We will use a trained tensorflow model to perform the classification')
        featureDict = predictor.featureSlider(item)
        predictor.makePrediction(featureDict)

if __name__ == '__main__':
    main(item=option)
