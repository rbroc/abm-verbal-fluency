import glob
from diversity_abm.agents import Agent
import itertools
import pandas as pd
import numpy as np
from diversity_abm import compute_thresholds
from diversity_abm import Interaction
from multiprocessing import Pool
import argparse
import warnings
warnings.filterwarnings("ignore")

# Date (used for logging)
date = '12_02_23'

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('--n-back', type=int, 
                    default=0,
                    help='n-back allowed')

# Load models
models = ['../diversity_abm/models/wiki_euclidean_distance.tsv']
animals = pd.read_csv('../diversity_abm/models/animal_list.csv')
thresholds = compute_thresholds(models, 
                                q=[round(n,2) for n in np.arange(0.05, 1.0, 0.05)], 
                                round_at=5)

# Load matrices and create agents
matrices = glob.glob(f'../diversity_abm/models/{date}/noised_distance_matrices/*')
dicts = [f'../diversity_abm/models/{date}/mappings/{f.split("/")[-1].strip(".tsv")}.json' 
           for f in matrices]
vects = [f'../diversity_abm/models/{date}/noised_vectors/{f.split("/")[-1]}' 
           for f in matrices]

agents = []
for i, m in enumerate(matrices):
    print(f'initializing agent {i}')
    agent = Agent(agent_name=m.split('/')[-1][:-4], 
                  matrix_filename=m, 
                  vector_filename=vects[i],
                  dict_filename=dicts[i])
    agents.append(agent)

# Interaction parameters
nr_sim = len(animals['Animals'].tolist())

# Main function
def run_individual(agent, outpath, n_back):

    print(f'Agent Name: {agent.name}')
    log_id = f'{agent.name}'
    i = Interaction(agents=agent,
                    threshold=thresholds[0.15], # Could be made flexible
                    save_folder=outpath,
                    log_id=log_id,
                    nr_sim=nr_sim,
                    kvals=[1,3,5])
    i.run_interaction(seeds=animals['Animals'].tolist(),
                      n_back=n_back)


if __name__=='__main__':
    pool = Pool(processes=60)
    args = parser.parse_args()
    nback_str = f'{args.n_back}_back'
    outpath = f'../diversity_abm/logs/{date}/{nback_str}/individual'
    outpaths = [outpath] * len(agents)
    pool.starmap(run_individual, zip(agents,
                                     outpaths,
                                     [args.n_back] * len(agents)))
    pool.close()
