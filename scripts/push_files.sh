#!/bin/bash

#afiles="../diversity_abm/analyses/12_02_23/*/*"
#git add $afiles
#git commit -m "add analysis files"
#git push origin main

#for i in {0..20..1}
#do
#   g="../diversity_abm/models/12_02_23/mappings/wiki_${i}_*"
#   echo "Adding ${i} mapping"
#   git add $g
#   git commit -m "add $i mapping individual"
#   git push origin main
#done

#for i in {0..20..1}
#do
#   g="../diversity_abm/models/12_02_23/noised_distance_matrices/wiki_${i}_*"
#   echo "Adding ${i} noised_distance_matrices"
#   git add $g
#   git commit -m "add $i noised_distance_matrices"
#   git push origin main
#done

#for i in {0..20..1}
#do
#   g="../diversity_abm/models/12_02_23/noised_vectors/wiki_${i}_*"
#   echo "Adding ${i} noised_vectors"
#   git add $g
#   git commit -m "add $i noised_vectors"
#   git push origin main
#done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/2_back/individual/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log individual"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/2_back/flexible/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log flexible"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/2_back/shortest/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log shortest"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/2_back/strict/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log strict"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/1_back/individual/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log individual"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/1_back/flexible/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log flexible"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/1_back/shortest/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log shortest"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/1_back/strict/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log strict"
   git push origin main
done


for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/0_back/individual/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log individual"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/0_back/flexible/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log flexible"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/0_back/shortest/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log shortest"
   git push origin main
done

for i in {0..20..1}
do
   g="../diversity_abm/logs/12_02_23/0_back/strict/wiki_${i}_*"
   echo "Adding ${i} log"
   git add $g
   git commit -m "add $i log strict"
   git push origin main
done

