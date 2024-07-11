from modules.commonModules import *
from predict import predictor
from explore import explorer


st.title('Iris Exploration and Prediction')

option = st.selectbox('Explore or Prediction Task',
                    ('Select Task', 'Explore', 'Predict'))


def main(item):
    item = item.lower()
    if item == "explore":
        #st.title('Sample data statistics')
        # st.dataframe(explorer.dataLoader())
        st.subheader('Univariant Analysis')
        explorer.getSummaries()
        st.subheader('Bivariant Analysis')
        explorer.getClassDistribution()
        explorer.getHeatmaps()
        pass
    elif item == 'predict':
        # predictor.featureSlider(item)
        featureDict = predictor.featureSlider(item)
        predictor.makePrediction(featureDict)

if __name__ == '__main__':
    main(item=option)
