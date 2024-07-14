from commonLibraries.libraries import *
import os

path = './datasets'
filename = 'customer_acquisition_data.csv'
file = os.path.join(path, filename)

def readFile():
    with open(file) as fopen:
        """
        We read the first line as columns and remove the new line character
        """
        allData = fopen.readlines()
        cols = allData[:1][0].strip().split(',')
        data = [line.strip().split(',') for line in allData[1:]]
        """
        We read each line into a list of dictionaries
        """
        datadict = [{cols[key]:val for key, val in enumerate(line)} for line in data]
        df = pd.DataFrame(datadict)
        """
        Since the data entries were all converted to strings, we convert all the other features to 
        and except for channel.
        """
        cols.remove('channel')
        for col in cols:
           df[col] =  df[col].astype(float)

        """
        We exclude the id feature since it does not add any value to the dataset.
        """
        return df.iloc[:, 1:]