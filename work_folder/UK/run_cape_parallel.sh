#!/usr/bin/env bash
set -euxo pipefail

N=2913

NJOBS=20

for i in $(seq 0 $((N-1))); do
  ./calc_xcape_UK.py "$i" &
  # throttle to  concurrent jobs
  # once we've kicked off ≥ NJOBS jobs, wait for *one* to finish
  if (( (i+1) >= NJOBS )); then
    wait -n
  fi
done


# wait for the remaining jobs
wait
