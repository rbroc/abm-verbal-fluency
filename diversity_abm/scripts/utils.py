import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances

def euclidean_distance(df, animal_list):
    ''' Compute euclidean distance between animal vectors '''
    emat = euclidean_distances(df.values, df.values)
    emat = pd.DataFrame(emat)
    emat.columns = animal_list.Animals.values
    emat.index = animal_list.Animals.values
    return emat