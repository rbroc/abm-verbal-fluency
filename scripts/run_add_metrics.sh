#sleep 6h
#cp ../diversity_abm/logs/12_02_23/2_back/flexible/* ../diversity_abm/logs/processed/2_back/flexible/*
#cp ../diversity_abm/logs/12_02_23/2_back/shortest/* ../diversity_abm/logs/processed/2_back/shortest/*
python3 add_metrics.py
