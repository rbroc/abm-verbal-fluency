import glob
import pandas as pd
import numpy as np
from multiprocessing import Pool
from diversity_abm import Agent

LOG_PATH = '../diversity_abm/logs/processed'
MODEL_PATH = '../diversity_abm/models/12_02_23/noised_distance_matrices'
files = glob.glob(LOG_PATH + '/*/*/*')

def add_metrics(f):
    print(f)
    df = pd.read_csv(f)
    condition = f.split('/')[5]
    if 'resp_knnd_5_a0_current' not in df.columns:
        log_id = df.log_id.tolist()[0]
        a0_name = '_'.join(log_id.split('_')[:3])
        a0 = Agent(agent_name=a0_name, 
                matrix_filename=MODEL_PATH + f'/{a0_name}.tsv')
        if condition != 'individual':
            a1_name = '_'.join(log_id.split('_')[3:6])
            a1 = Agent(agent_name=a1_name, 
                    matrix_filename=MODEL_PATH + f'/{a1_name}.tsv')
        
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

        new_metrics = []
        for _, row in df.iterrows():
            if row['seed'] == row['init_seed']:
                a0.matrix.data = a0.matrix_backup.data.copy()
                if condition != 'individual':
                    a1.matrix.data = a1.matrix_backup.data.copy()
            new_metrics_row = []
            a0._pop_words(row['seed'])
            if condition != 'individual':
                a1._pop_words(row['seed'])
            for k in [1,3,5]:
                new_metrics_row.append((1/np.sort(a0.matrix.data[row['response']])[k]).round(5))
                if condition != 'individual':
                    new_metrics_row.append((1/np.sort(a1.matrix.data[row['response']])[k]).round(5))
            new_metrics_row.append((a0.matrix_backup.data[row['response']]<0.01179).sum())
            if condition != 'individual':
                new_metrics_row.append((a1.matrix_backup.data[row['response']]<0.01179).sum())
            new_metrics_row.append((a0.matrix.data[row['response']]<0.01179).sum())
            if condition != 'individual':
                new_metrics_row.append((a1.matrix.data[row['response']]<0.01179).sum())
            new_metrics.append(new_metrics_row)
        new_metrics_df = pd.DataFrame(new_metrics, columns=colnames)
        old_col = df.columns
        df = pd.concat([df,new_metrics_df], axis=1, ignore_index=True)
        df.columns = old_col.tolist() + colnames
        df.to_csv(f, index=False)

if __name__=='__main__':
    pool = Pool(60)
    pool.map(add_metrics, files)
    pool.close()