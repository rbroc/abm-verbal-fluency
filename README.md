# ABM of word association game 
This repository contains the code to run agent-based simulations of a word association game performed either individually or interactively by agents of varying diversity, whose semantic memories are noised versions of a skip-gram word2vec model.

The repository includes:
- ```diversity_abm```
    - Code for the mechanisms of the simulation;
- ```baseline.ipynb```
    - Notebook to run and analyse baseline performance (of the non-noised word2vec agent);
- ```noise_and_pair.ipynb```
    - Code to add varying levels of noise to the word2vec model and generate agents of different "diversity levels";
- ```analysis.ipynb``` and ```supplementary.ipynb```
    - analysis of the effect of interaction and diversity on different metrics of creativity in the association behavior produced by agents/pairs.
    
A first version of this is published as CogSci proceedings: https://escholarship.org/uc/item/58v5d82w, cite as: Rocca, R., & Tylén, K., 2022, Cognitive diversity promotes collective creativity: an agent-based simulation, *Proceedings of the Annual Meeting of the Cognitive Science Society*, 44

A follow-up is in progress.

____________

**Current setup with n-back agents**
- *Strict*: if agent does not find associations in n-back turns, trial is over;
- *Flexible*: if current agent does not find association in n-back turns, turn is handed over to the other agent
    - Note, instead of nesting the n-back logic inside the flexible interaction logic, one could do the other way round;
- *Shortest*: for each seed, give word to the agent with shortest association. If no sub-threshold values are available, go one seed back and repeat.

