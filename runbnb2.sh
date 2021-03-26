#!/bin/bash
for i in 400 600 800 1000; do
    for filename in tsp-problem-${i}-*.txt; do
        python3 main.py $filename
    done
done
