import pandas as pd
import numpy as np
import glob

animals = pd.read_csv(f'../diversity_abm/models/animal_list.csv')
animals_idx_dict = dict(zip(animals['Animals'].tolist(),
                        [str(i) for i in range(len(animals))]))

# Dictionaries for aggregation turn -> trial-level
INDIVIDUAL_DICT = {'turn': 'max',
                   'threshold': 'first',
                   'agent': 'first',
                   'init_seed': 'first',
                   'prob0': np.nanmean,
                   'ndens_0': np.nanmean,
                   'ndens_current_0': np.nanmean,
                   'response': 'last'}
PAIR_DICT = {'turn': 'max', 
             'log_id': 'first',
             'agent_0': 'first',
             'agent_1': 'first',
             'threshold':'first',
             'init_seed': 'first',
             'prob0': np.nanmean,
             'prob1': np.nanmean,
             'jump_speaker': np.nanmean,
             'jump_listener': np.nanmean,
             'response': 'last'}

# Column names for metrics above
INDIVIDUAL_NAMES = ['iter', 'performance', 'threshold', 
                    'agent_name', 'init_seed', 
                    'flexibility',
                    'last_response']
PAIR_NAMES = ['iter', 'performance', 'pair',
              'agent_0', 'agent_1',
              'threshold', 'init_seed',
              'flexibility_0',
              'flexibility_1', 
              'flexibility_speaker', 
              'flexibility_listener',
              'last_response']

# Rename columns that have the same name across individual and pair
RENAME_0 = {'performance_x': 'performance_pair',
            'performance_y': 'performance_a0',
            'noise_level_y': 'noise_level_a0',
            'flexibility': 'flexibility_a0',
            'last_response_x': 'last_response_pair',
            'last_response_y': 'last_response_a0'}
RENAME_1 = {'performance': 'performance_a1',
            'flexibility': 'flexibility_a1',
            'last_response': 'last_response_a1',
            'noise_level': 'noise_level_a1'}


# Define dictionaries for aggregation trial -> pair-level
PAIR_LEVEL_DICT = {'diversity_level': np.nanmean,
                   'fluency_a0': np.nanmean,
                   'fluency_a1': np.nanmean,
                   'fluency_best': np.nanmean,
                   'fluency_pair': np.nanmean,
                   'fluency_gain': [np.nanmean, np.nanstd],
                   'flexibility_speaker': np.nanmean,
                   'flexibility_listener': np.nanmean,
                   'flexibility_a0': np.nanmean,
                   'flexibility_a1': np.nanmean,
                   'flexibility_best': np.nanmean,
                   'flexibility_gain': [np.nanmean, np.nanstd],
                   'orig_pair': np.nanmean,
                   'orig_gain': [np.nanmean, np.nanstd],
                   'orig_a0': np.nanmean,
                   'orig_a1':np.nanmean,
                   'orig_best':np.nanmean,
                   'collective_inhibition': [np.nanmean, np.nanstd]}

# Define names for columns aggregated with dict above
PAIR_LEVEL_NAMES = ['pair', 
                    'diversity_level',
                    'fluency_a0',
                    'fluency_a1',
                    'fluency_best',
                    'fluency_pair',
                    'fluency_gain_trial',
                    'fluency_gain_trial_std',
                    'flexibility_speaker', 
                    'flexibility_listener',
                    'flexibility_a0',
                    'flexibility_a1',
                    'flexibility_best',
                    'flexibility_gain_trial',
                    'flexibility_gain_trial_std',
                    'orig_pair',
                    'orig_gain_trial',
                    'orig_gain_trial_std',
                    'orig_a0',
                    'orig_a1',
                    'orig_best',
                    'collective_inhibition',
                    'collective_inhibition_std']


def get_individual_aggs(f):
    ''' Function to compute aggregates in individual performance data'''
    log = pd.read_csv(f)
    ind_agg = log.groupby('iter').agg(INDIVIDUAL_DICT).reset_index()
    ind_agg.columns = INDIVIDUAL_NAMES
    try:
        ind_agg['noise_level'] = ind_agg['agent_name'].str.split('_').str[1].astype(float)
    except:
        ind_agg['noise_level'] = -1.0
    return ind_agg


def get_pair_aggs(f):
    ''' Function to compute aggregates in pair performance data'''
    log = pd.read_csv(f)
    log['agent_0'] = log['log_id'].str.split('_').str[:3].str.join('_').iloc[0]
    log['agent_1'] = log['log_id'].str.split('_').str[3:].str.join('_').iloc[0]
    log['agent_speaking'] = np.where(log['agent']==log['agent_0'], 
                                     'agent_0', 
                                     'agent_1')
    log['jump_speaker'] = np.where(log['agent_speaking']=='agent_0', 
                                   log['prob0'], 
                                   log['prob1'])
    log['jump_listener'] = np.where(log['agent_speaking']=='agent_0', 
                                    log['prob1'], 
                                    log['prob0'])
    log['pos_response'] = np.where(log['agent_speaking']=='agent_0', 
                                   log['pos_response_0'], 
                                   log['pos_response_1'])
    log['jump_difference'] = log['jump_listener'] - log['jump_speaker']
    pair_agg = log.groupby('iter').agg(PAIR_DICT).reset_index()
    pair_agg.columns = PAIR_NAMES
    pair_agg['noise_level'] = pair_agg['agent_0'].str.split('_').str[1].astype(float)
    return pair_agg


def concat_dfs(result_list):
    ''' Concatenate dataframes in list as single df'''
    for idx, r in enumerate(result_list):
        if idx == 0:
            out = r
        else:
            out = pd.concat([out, r], 
                            ignore_index=True)
    return out


def merge_pairs_inds(pdf, idf, agent_nr):
    ''' Merge df of pair aggregate metrics with individual aggregates '''
    pdf = pdf.merge(idf, 
                    right_on=['agent_name', 'init_seed'],
                    left_on=[f'agent_{agent_nr}', 'init_seed'],
                    how='outer').drop(['agent_name'], axis=1)
    if agent_nr == '0':
        pdf.drop('noise_level_x', axis=1, inplace=True)
        pdf = pdf.rename(RENAME_0, axis=1)
    else:
        pdf.drop('noise_level', axis=1, inplace=True)
        pdf = pdf.rename(RENAME_1, axis=1)
    return pdf


def get_unique_named(f, LOG_PATH, date, n_back, threshold=0.01179): # replace threshold
    '''
        Get dataframe with number of unique words named per trial, 
        both for pairs (= performance) and for concatenated lists
        of animals named by individuals 
    '''
    log = pd.read_csv(f)
    pair_id = log.log_id.iloc[0]
    pair_counts = log.groupby('init_seed').response.count().reset_index()
    pair_counts = pair_counts.rename({'response': 
                                      'unique_pair'}, axis=1)
    a0_name = log['log_id'].str.split('_').str[:3].str.join('_').iloc[0]
    a1_name = log['log_id'].str.split('_').str[3:].str.join('_').iloc[0]
    IND_PATH = f'{LOG_PATH}/{date}/{n_back}_back'
    a0_log = pd.read_csv(f'{IND_PATH}/individual/{a0_name}_1_{threshold}.txt')
    a1_log = pd.read_csv(f'{IND_PATH}/individual/{a1_name}_1_{threshold}.txt')
    a0_list = a0_log.groupby('init_seed').agg({'response': list}).reset_index()
    a1_list = a1_log.groupby('init_seed').agg({'response': list}).reset_index()
    counts = a0_list.merge(a1_list, on='init_seed')
    counts['unique_individual'] = (counts['response_x'] + \
                                   counts['response_y']).apply(lambda x: len(set(x)))
    counts = counts.drop(['response_x', 'response_y'], axis=1)
    counts = pair_counts.merge(counts, on='init_seed')
    counts['pair'] = pair_id
    return counts


def get_wd_originality_scores(f):
    ''' Compute the originality score for each word '''
    data = pd.read_csv(f)
    counts = data.groupby('pos_response_0')['agent'].count().reset_index()
    counts.columns = ['word', 'count']
    return counts


def _process_originality_df(log, merge_col, idx, wd_orig, 
                            individual=False):
    ''' Process datasets for originality '''
    left_col = 'pos_response' if individual == False else 'pos_response_0'
    merged = log.merge(wd_orig[merge_col], 
                       left_on=left_col, 
                       right_on='word').drop('word', axis=1)
    merged = merged.groupby('init_seed').agg({'originality_score': 
                                              np.nanmean}).reset_index()
    merged.columns = ['init_seed', f'orig_{idx}']
    return merged

    
def get_originality(f, wd_orig, LOG_PATH, date, n_back, threshold=0.01179):
    ''' Compute avg originality for individuals and pairs '''
    # Process pair
    merge_col = ['word', 'originality_score']
    log = pd.read_csv(f)
    log['agent_0'] = log['log_id'].str.split('_').str[:3].str.join('_').iloc[0]
    log['agent_1'] = log['log_id'].str.split('_').str[3:].str.join('_').iloc[0]
    log['agent_speaking'] = np.where(log['agent']==log['agent_0'], 
                                     'agent_0', 
                                     'agent_1')
    log['pos_response'] = np.where(log['agent_speaking']=='agent_0', 
                                   log['pos_response_0'], 
                                   log['pos_response_1'])
    pair_id = log.log_id.iloc[0]
    merged_pair = _process_originality_df(log, merge_col, 'pair', wd_orig)
    merged_pair['pair'] = pair_id
    # Process individual
    a0_name = log['log_id'].str.split('_').str[:3].str.join('_').iloc[0]
    IND_PATH = f'{LOG_PATH}/{date}/{n_back}_back'
    a0_log = pd.read_csv(f'{IND_PATH}/individual/{a0_name}_1_{threshold}.txt')
    a1_name = log['log_id'].str.split('_').str[3:].str.join('_').iloc[0]
    a1_log = pd.read_csv(f'{IND_PATH}/individual/{a1_name}_1_{threshold}.txt')
    merged_a0 = _process_originality_df(a0_log, merge_col, 'a0', wd_orig, individual=True)
    merged_a1 = _process_originality_df(a1_log, merge_col, 'a1', wd_orig, individual=True)
    # Merge stuff
    merged_pair = merged_pair.merge(merged_a0, on='init_seed')
    merged_pair = merged_pair.merge(merged_a1, on='init_seed')
    return merged_pair



def add_metrics(df): 
    df.rename({'noise_level_a0': 'diversity_level',
               'performance_a0': 'fluency_a0',
               'performance_a1': 'fluency_a1',
               'performance_pair': 'fluency_pair'}, axis=1,
               inplace=True)
    df['fluency_best'] = np.where(df['fluency_a1']>\
                                  df['fluency_a0'], 
                                  df['fluency_a1'],
                                  df['fluency_a0']).astype(int)
    df['flexibility_best'] = np.where(df['flexibility_a0']>\
                                      df['flexibility_a1'],
                                      df['flexibility_a0'], 
                                      df['flexibility_a1'])
    df['orig_best'] = np.where(df['orig_a1']>df['orig_a0'], 
                               df['orig_a1'],
                               df['orig_a0'])
    df['fluency_gain'] = df['fluency_pair'] / df['fluency_best'] 
    df['fluency_gain'] = (df['fluency_gain'] - 1) * 100 
    df['flexibility_gain'] = df['flexibility_speaker'] / df['flexibility_best'] 
    df['flexibility_gain'] = (df['flexibility_gain'] - 1) * 100 
    df['orig_gain'] = ((df['orig_pair'] / df['orig_best']) - 1) * 100 
    return df



def get_pair_level_aggregates(pdf):
    ''' Compute pair-level aggregates '''
    aggs = pdf.groupby('pair').agg(PAIR_LEVEL_DICT).reset_index()
    aggs.columns = PAIR_LEVEL_NAMES
    aggs['fluency_gain_tot'] = aggs['fluency_pair'] / aggs['fluency_best']
    aggs['flexibility_gain_tot'] = aggs['flexibility_speaker'] / aggs['flexibility_best']
    aggs['orig_gain_tot'] = np.where(aggs['orig_a0'] > aggs['orig_a1'], 
                                     aggs['orig_pair'] / aggs['orig_a0'],
                                     aggs['orig_pair'] / aggs['orig_a1'])
    for metric in ['fluency_gain_tot', 
                   'flexibility_gain_tot',  
                   'orig_gain_tot']:
        aggs[metric] = (aggs[metric] - 1) * 100
    return aggs
