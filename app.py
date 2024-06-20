from modules.commonModules import *
from predict import predictor
from explore import explorer


st.title('Test app')
st.markdown("""
Sample prediction tasks
""")

option = st.selectbox('Make a selection',
                    ('Select option', 'Explore', 'Predict'))


def main(item):
    item = item.lower()
    if item == "explore":
        st.title('Sample data statistics')
        # st.dataframe(explorer.dataLoader())
        explorer.getSummaries()
        st.title('Sample data distribution')
        explorer.getClassDistribution()
        pass
    elif item == 'predict':
        # predictor.featureSlider(item)
        featureDict = predictor.featureSlider(item)
        predictor.makePrediction(featureDict)

if __name__ == '__main__':
    main(item=option)
