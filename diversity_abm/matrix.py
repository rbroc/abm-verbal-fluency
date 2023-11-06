import pandas as pd 
import numpy as np 
from .utils import load_matrix

class Matrix:
    ''' Semantic memory of Agent
    Args:
        filename (str): file where similarity matrix is stored
        path (str): relative path to folder where matrix is located
        name (str, optional): optional name for model (if None, uses filename)
            If 'softmax', scales scores using softmax. If 'sum', divides by
            sum of values. If None, leaves as-is.
        kwargs: named arguments for transform_function call.
    '''
    def __init__(self, filename, path=None, name=None):
        model = load_matrix(filename=filename, path=path)
        self.data = model.copy()
        self.name = name or filename.strip('.csv')

    @property
    def words(self):
        return list(self.data.index)
