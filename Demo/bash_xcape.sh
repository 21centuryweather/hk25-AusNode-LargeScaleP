#!/usr/bin/env bash
set -euxo pipefail

N=58
YEAR=1940

NJOBS=28

for i in $(seq 0 $((N-1))); do
  ./calc_xcape.py "$i" "$YEAR" &
  # throttle to  concurrent jobs
  # once we've kicked off ≥ NJOBS jobs, wait for *one* to finish
  if (( (i+1) >= NJOBS )); then
    wait -n
  fi
done


# wait for the remaining jobs 
wait
