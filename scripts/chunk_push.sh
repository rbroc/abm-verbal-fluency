#!/bin/bash
start_commit=dcb82264fec14a75663548caa413307f22f726e5
commit_hashes=$(git log --oneline $start_commit..HEAD --format="%h")
for commit_hash in $commit_hashes
do
   git push origin $commit_hash:master
done




