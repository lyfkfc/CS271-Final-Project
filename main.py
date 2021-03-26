# Traveling Salesman Problem using
# Branch and Bound.
import time
import sys
import signal

sys.setrecursionlimit(1500)
maxsize = float('inf')
numdrop = 0
numupdate = 0
t_end = time.time() + 15 #15 minutes cap

# Copy path to final_path
def copyToFinal(curr_path):
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]

# first Min
def firstMin(adj, i):
    min = maxsize
    for k in range(N):
        if adj[i][k] < min and i != k:
            min = adj[i][k]

    return min

# second Min
def secondMin(adj, i):
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]

        elif(adj[i][j] <= second and
             adj[i][j] != first):
            second = adj[i][j]

    return second

# recursion function for BnB
def TSPRec(adj, curr_bound, curr_weight,
           level, curr_path, visited):
    global final_res
    global numupdate
    global numdrop
    if time.time() >= t_end:
        return
    # base case is when we have reached level N
    # which means we have covered all the nodes once
    if level == N:

        # check if there is an edge from
        # last vertex in path back to the first vertex
        if adj[curr_path[level - 1]][curr_path[0]] != 0:

            # curr_res has the total weight
            # of the solution we got
            curr_res = curr_weight + adj[curr_path[level - 1]] \
                [curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res
                print("Min path updated to: ", curr_res)
                numupdate+=1
        return


    for i in range(N):

        # dfs to connected cities
        if (adj[curr_path[level-1]][i] != 0 and
                visited[i] == False):
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]

            # different computation of curr_bound
            # for level 2 from the other levels
            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)

            #pruning condition
            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True

                TSPRec(adj, curr_bound, curr_weight,
                       level + 1, curr_path, visited)

            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp
            numdrop += 1

            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True

def TSP(adj):

    curr_bound = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N

    for i in range(N):
        curr_bound += (firstMin(adj, i) +
                       secondMin(adj, i))

    curr_bound = curr_bound / 2


    visited[0] = True
    curr_path[0] = 0

    TSPRec(adj, curr_bound, 0, 1, curr_path, visited)


adj = []
numOfCity=0
# with open("tsp-problem-25-6-100-5-1.txt") as f:

with open(sys.argv[1]) as f:
    numOfCity = int(f.readline().strip())
    for line in f:
        number_strings = line.split()
        numbers = [float(n) for n in number_strings]
        adj.append(numbers)
print(numOfCity)
# print(len(adj),len(adj[0]))
N = numOfCity

final_path = [None] * (N + 1)

visited = [False] * N

final_res = maxsize

TSP(adj)

print("Minimum cost :", final_res)
print("Path Taken : ", end = ' ')
for i in range(N + 1):
    print(final_path[i], end = ' ')

f = open('bnbresult.csv','a')
f.write("%s " % sys.argv[1])
s=""
for path in final_path:
    s+=str(path)
    s+='-'
f.write("%.13f " % final_res)
f.write(s)
f.write(" %d" % numupdate)
f.write(" %d" % numdrop)
f.write('\n')
## Python will convert \n to os.linesep
f.close()
