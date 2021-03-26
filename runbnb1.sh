#!/bin/bash
for i in 25 50 75 100 200; do
    for filename in tsp-problem-${i}-*.txt; do
        python3 main.py $filename
    done
done
