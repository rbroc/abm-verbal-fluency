import pandas as pd 
import numpy as np 
from .utils import load_matrix
from .matrix import Matrix
import json
from copy import deepcopy

class Agent:
    ''' Initializes an agent
    Args:
        name (str): specifies an ID for the agent
        matrix_filename (str): path to agent's model.
        path (str or Path): folder to agent's model in current wd.
        matrix_kwargs: named arguments for Matrix initialization
    '''

    def __init__(self, agent_name, matrix_filename,
                 dict_filename=None,
                 vector_filename=None,
                 path=None,
                 **matrix_kwargs):
        self.name = agent_name or matrix_filename
        self.matrix = Matrix(filename=matrix_filename, path=path,
                             **matrix_kwargs)
        self.matrix_backup = deepcopy(self.matrix)
        if dict_filename:
            self.position_map = json.load(open(dict_filename, 'r'))
        else:
            self.position_map = None
        if vector_filename:
            self.vectors = pd.read_csv(vector_filename, sep='\t', index_col=0)
        else:
            self.vectors = None

    @property
    def model(self):
        return self.matrix.data
    
    def get_metrics(self, resp_wd, kvals):
        ''' Returns spatial metrics for a turn '''
        knn_dist_resp = [(1/np.sort(self.matrix_backup.data[resp_wd])[k]).round(5)
                         for k in kvals]
        avg_dist_remain = self.matrix.data.mean(axis=0).mean().round(5)
        mean_knn_dists = [np.partition(self.matrix.data, kth=k, axis=0)[k,:].mean().round(5)
                          for k in kvals]
        var_knn_dists = [np.partition(self.matrix.data, kth=k, axis=0)[k,:].std().round(5)
                          for k in kvals]
        return [*knn_dist_resp, 
                avg_dist_remain, 
                *mean_knn_dists, 
                *var_knn_dists]

    def speak(self, seed, pop=True):
        ''' Picks response word based on cue (seed).
            Returns probability of cue-response association, and response word.
            Also pops response/cue value if pop=True
        '''
        resp_idx = np.argmin(self.matrix.data[seed])
        resp_wd = self.matrix.data[seed].index[resp_idx]
        prob = self.listen(seed, resp_wd, pop)
        return round(prob,5), resp_wd

    def listen(self, seed, resp_wd, pop=True):
        ''' Listens to response (resp_wd), return probability of response
            given the cue in the agent's space and pops response/cue value
            from agent's memory is pop is true
        '''
        prob = self._return_prob(seed, resp_wd)
        if pop:
            self._pop_words(resp_wd)
        return round(prob,5)

    def _return_prob(self, seed, resp_wd, pop=True):
        ''' Returns association score for seed-resp_wd pair '''
        return self.matrix.data[seed][resp_wd]

    def _pop_words(self, resp_wd):
        ''' Pop response word for possible options '''
        self.matrix.data.loc[resp_wd] = np.nan

    def get_vector_var(self, words):
        ''' Returns variance within dimensions '''
        return self.vectors.loc[words].values.var(axis=0).mean().round(5)
