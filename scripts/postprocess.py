import glob
import itertools
import pandas as pd
import numpy as np
from utils import (get_individual_aggs, 
                   get_pair_aggs,
                   concat_dfs, 
                   merge_pairs_inds, 
                   get_unique_named,
                   get_wd_originality_scores,
                   get_originality,
                   add_metrics,
                   get_pair_level_aggregates)
from multiprocessing import Pool
from sklearn.preprocessing import MinMaxScaler
from itertools import product
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--interaction-type', type=str, 
                    default='strict',
                    help='strict, flexible or shortest')
parser.add_argument('--n-back', type=int, default=0)

DATE = '12_02_23'  #28, 30
MODELS_PATH = '../diversity_abm/models'
LOG_PATH = '../diversity_abm/logs'
AN_PATH = '../diversity_abm/analyses'
scaler = MinMaxScaler()


def _get_aggs(fn, flist):
    pool = Pool(20)
    results = pool.map(fn, flist)
    pool.close()
    aggs = concat_dfs(results)
    return aggs
 
    
def _merge_aggs(pdf, idf):
    if all([i in idf.columns for i in ['iter', 'threshold']]):
        idf.drop(['iter', 'threshold'], axis=1, inplace=True)
    if all([p in pdf.columns for p in ['iter', 'threshold']]):
        pdf.drop(['iter', 'threshold'], axis=1, inplace=True)
    pdf = merge_pairs_inds(pdf, idf, '0')
    pdf = merge_pairs_inds(pdf, idf, '1')
    return pdf


def _get_unique_named(flist, pdf, n_back):
    pool = Pool(20)
    results = pool.starmap(get_unique_named, zip(flist,
                                                 [LOG_PATH]*len(flist),
                                                 [DATE]*len(flist),
                                                 [n_back]*len(flist)))
    pool.close()
    unique_named = concat_dfs(results)
    pdf = pdf.merge(unique_named, 
                    on=['init_seed', 'pair'], how='outer')
    pdf['collective_inhibition'] = pdf['unique_individual'] - pdf['unique_pair']
    pdf['collective_inhibition'] = (pdf['collective_inhibition']) / 240 * 100
    return pdf


def _get_originality(iflist, pflist, pdf, n_back):
    pool = Pool(20)
    results = pool.map(get_wd_originality_scores, iflist)
    pool.close()
    wd_orig = concat_dfs(results)
    wd_orig = wd_orig.groupby('word')['count'].sum().reset_index()
    wd_orig['originality_score'] = ((240 * 100 * 21 * 3) - wd_orig['count']) / (240 * 100 * 21 * 3) # 20
    pool = Pool(20)
    results = pool.starmap(get_originality, zip(pflist,
                                                [wd_orig]*len(pflist),
                                                [LOG_PATH]*len(pflist),
                                                [DATE]*len(pflist),
                                                [n_back]*len(pflist)))
    pool.close()
    orig_df = concat_dfs(results)
    pdf = pdf.merge(orig_df, on=['init_seed', 'pair'], how='outer')
    return pdf


def postprocess(int_str, n_back):
    
    # Get filenames
    fs_all = glob.glob(f'{LOG_PATH}/{DATE}/*/individual/*')
    fs = glob.glob(f'{LOG_PATH}/{DATE}/{n_back}_back/individual/*')
    pair_fs = glob.glob(f'{LOG_PATH}/{DATE}/{n_back}_back/{int_str}/*')
    
    # Get aggregates
    print('*** Computing aggregates ***')
    ia = _get_aggs(get_individual_aggs, fs)
    pa = _get_aggs(get_pair_aggs, pair_fs)
    
    # Add all missing trials
    animals = pa.init_seed.unique().tolist()
    pairs = pa.pair.unique().tolist()
    agents = ia.agent_name.unique().tolist()
    full_df = pd.DataFrame(list(product(pairs, animals)), 
                           columns=['pair', 
                                    'init_seed'])
    full_df['agent_0'] = full_df['pair'].str.split('_').str[:3].str.join('_')
    full_df['agent_1'] = full_df['pair'].str.split('_').str[3:].str.join('_')
    pa = pa.merge(full_df, on=['pair', 
                               'init_seed', 
                               'agent_0', 
                               'agent_1'], how='outer')
    full_df_ind = pd.DataFrame(list(product(agents, animals)), 
                               columns=['agent_name', 
                                        'init_seed'])
    ia = ia.merge(full_df_ind, on=['agent_name', 
                                   'init_seed'], how='outer')
    pa = _merge_aggs(pa, ia)
    for c in ['a1', 'a0', 'pair']:
        pa[f'performance_{c}'] = pa[f'performance_{c}'].fillna(0)
    
    print('*** Computing collective inhibition metrics ***')
    pa = _get_unique_named(pair_fs, pa, n_back)

    print('*** Computing originality ***')
    pa = _get_originality(fs_all, pair_fs, pa, n_back)
    
    # Add metrics, compute aggregates, and save
    print('*** Summarizing ***')
    pa = add_metrics(pa)
    # Add for each pair 
    aggs = get_pair_level_aggregates(pa)
    
    # Add metadata & Save
    print('*** Saving ***')
    pa['n_back'] = n_back
    aggs['n_back'] = n_back
    pa['interaction_type'] = int_str
    aggs['interaction_type'] = int_str
    pa.to_csv(f'{AN_PATH}/{DATE}/{n_back}_back/processed_{int_str}.tsv',
              sep='\t', 
              index=False)
    aggs.to_csv(f'{AN_PATH}/{DATE}/{n_back}_back/aggregates_{int_str}.tsv',
                sep='\t', 
                index=False) 
                            
                            
if __name__=='__main__':
    args = parser.parse_args()
    postprocess(args.interaction_type, args.n_back)
                            
