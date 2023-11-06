python3 run_individual.py --n-back 0
python3 run_individual.py --n-back 1
python3 run_individual.py --n-back 2
python3 run_pairs.py --n-back 0 --interaction-type strict
python3 run_pairs.py --n-back 1 --interaction-type strict # half of this
python3 run_pairs.py --n-back 2 --interaction-type strict
python3 run_pairs.py --n-back 0 --interaction-type flexible
python3 run_pairs.py --n-back 1 --interaction-type flexible
python3 run_pairs.py --n-back 2 --interaction-type flexible
python3 run_pairs.py --n-back 0 --interaction-type shortest
python3 run_pairs.py --n-back 1 --interaction-type shortest
python3 run_pairs.py --n-back 2 --interaction-type shortest
