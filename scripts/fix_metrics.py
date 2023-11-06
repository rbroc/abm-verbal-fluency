import glob
import pandas as pd
import numpy as np
from multiprocessing import Pool
from diversity_abm import Agent

LOG_PATH = '../diversity_abm/logs/processed'
MODEL_PATH = '../diversity_abm/models/12_02_23/noised_distance_matrices'
VEC_PATH = '../diversity_abm/models/12_02_23'
files = glob.glob(LOG_PATH + '/*/*/*')

def add_metrics_2(f):
    try:
        df = pd.read_csv(f)
        condition = f.split('/')[5]
        if ((condition == 'individual' and len(df.columns)==30) or (condition != 'individual' and len(df.columns)==49)): # if it has been processed
            print(f)
            colnames = []
            if condition != 'individual':
                for k in [1,3,5]:
                    for a in ['a0', 'a1']:
                        colnames.append(f'resp_knnd_{k}_{a}_current')
                colnames += ['resp_neighbors_a0', 
                            'resp_neighbors_a1']
                colnames += ['resp_neighbors_a0_current', 
                            'resp_neighbors_a1_current']
            else:
                for k in [1,3,5]:
                    colnames.append(f'resp_knnd_{k}_a0_current')
                colnames += ['resp_neighbors_a0', 
                            'resp_neighbors_a0_current']
            if condition != 'individual':
                old_col = ['agent','turn','iter','seed','response','prob0','prob1','pos_init_seed_0','pos_init_seed_1','pos_response_0','pos_response_1','threshold','nr_sim','max_exchanges','init_seed','log_id','nr_agents','resp_knnd_1_a0','resp_knnd_3_a0','resp_knnd_5_a0','avg_dist_remain_a0','avg_knnd_1_a0','avg_knnd_3_a0','avg_knnd_5_a0','var_knnd_1_a0','var_knnd_3_a0','var_knnd_5_a0','resp_knnd_1_a1','resp_knnd_3_a1','resp_knnd_5_a1','avg_dist_remain_a1','avg_knnd_1_a1','avg_knnd_3_a1','avg_knnd_5_a1','var_knnd_1_a1','var_knnd_3_a1','var_knnd_5_a1','vecvar_a0','vecvar_a1']
            else:
                old_col = ['agent','turn','iter','seed','response','prob0','pos_init_seed_0','pos_response_0','threshold','nr_sim','max_exchanges','init_seed','log_id','nr_agents','resp_knnd_1_a0','resp_knnd_3_a0','resp_knnd_5_a0','avg_dist_remain_a0','avg_knnd_1_a0','avg_knnd_3_a0','avg_knnd_5_a0','var_knnd_1_a0','var_knnd_3_a0','var_knnd_5_a0','vecvar_a0']
            df.columns = old_col + colnames
            df.to_csv(f, index=False)
        else:
            print(f'{f} has {len(df.columns)} columns')
    except:
        print(f'Failed {f}')
        print(len(old_col))
        print(len(colnames))
        raise ValueError

if __name__=='__main__':
    pool = Pool(60)
    pool.map(add_metrics_2, files)
    pool.close()