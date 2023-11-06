#!/bin/bash

python3 postprocess.py --interaction-type strict --n-back 0
python3 postprocess.py --interaction-type flexible --n-back 0
python3 postprocess.py --interaction-type shortest --n-back 0
python3 postprocess.py --interaction-type strict --n-back 1
python3 postprocess.py --interaction-type flexible --n-back 1
python3 postprocess.py --interaction-type shortest --n-back 1
python3 postprocess.py --interaction-type strict --n-back 2
python3 postprocess.py --interaction-type flexible --n-back 2
python3 postprocess.py --interaction-type shortest --n-back 2
cd ../diversity_abm/analyses/12_02_23/0_back
gzip processed_strict.tsv -f
gzip processed_flexible.tsv -f
gzip processed_shortest.tsv -f
cd ../1_back
gzip processed_strict.tsv -f 
gzip processed_flexible.tsv -f
gzip processed_shortest.tsv -f
cd ../2_back
gzip processed_strict.tsv -f 
gzip processed_flexible.tsv -f 
gzip processed_shortest.tsv -f
cd ../../../../scripts
