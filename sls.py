import numpy as np
import matplotlib.pyplot as plt
import numpy.random as random
import time
import csv
import os

TIME_LIMIT = 60 * 2

def get_random_path(best_path):
    random.shuffle(best_path)
    path = np.append(best_path, best_path[0])
    return path

def calculate_path_distance(path, input):
    sum = 0.0
    for i in range(1, len(path)):
        sum += input[path[i-1]][path[i]]
    return sum

def get_reverse_path(path):
    start = random.randint(1, len(path) - 1)
    while True:
        end = random.randint(1, len(path) - 1)
        if np.abs(start - end) > 1:
            break

    if start > end:
        path[end: start+1] = path[end: start+1][::-1]
        return path
    else:
        path[start: end+1] = path[start: end+1][::-1]
        return path

def compare_paths(path_one, path_two, input):
    return calculate_path_distance(path_one, input) > calculate_path_distance(path_two, input)

def update_path(path, input):
    run_time = 0
    num_updates = 0
    num_search = 0
    while run_time < TIME_LIMIT:
        start_time = time.clock()
        num_search += 1
        reverse_path = get_reverse_path(path.copy())
        if compare_paths(path, reverse_path, input):
            count = 0
            path = reverse_path
            num_updates += 1
        run_time += time.clock() - start_time
    return path, num_updates, num_search

def file2array(path, delimiter=' '):
    fp = open(path, 'r', encoding='utf-8')
    string = fp.read()
    fp.close()
    row_list = string.splitlines()
    n = row_list[0]
    row_list = row_list[1:]
    data_list = [[float(i) for i in row.strip().split(delimiter)] for row in row_list]
    return np.array(data_list), n

def main():
    out_path = "results2.csv"
    info = [["yfgeng2,"], ["SLS"], ["TSP"]]
    output = open(out_path, 'w')
    csvwriter = csv.writer(output)
    csvwriter.writerows(info)

    for file in os.listdir("fall20-benchmark-tsp-problems"):
        path = "fall20-benchmark-tsp-problems/" + file
        input, n = file2array(path, ' ')
        best_path = np.arange(len(input))
        start_time = time.clock()
        best_path = get_random_path(best_path)
        num_updates = 0
        num_search = 0
        path, num_updates, num_search = update_path(best_path, input)
        best_length = calculate_path_distance(path, input)
        ans = [file, best_length, num_updates, num_search]
        csvwriter.writerow(ans)
        print("Searching case " + file + " has been completed!")

if __name__ == "__main__":
    main()
