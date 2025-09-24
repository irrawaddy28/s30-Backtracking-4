'''
Optimal Placement of Buildings in a grid (not a leetcode problem)

Given a grid with w as width, h as height. Each cell of the grid represents a potential building lot and we will be adding "n" buildings inside this grid. The goal is for the furthest of all buildings to be as near as possible to an empty lot (for eg. parking lot).
That is, if there are n=3 buildings, and
di = distance between building i and parking lot, i = 1, 2, 3
then the objective to minimize max(d1, d2, d3). In other words, find the position of d1, d2, d3 such that min (max(d1, d2, d3)). For hw buildings,
n buildings can be chosen in hw C n ways. We want to find the min of those hw C n ways.

Given an input n, which is the number of buildings to be placed in the lot, determine the building placement to minimize the distance between the most distant parking lot from the building. Movement is restricted to horizontal and vertical i.e. diagonal movement is not required.

For example, w=4, h=4 and n=3. An optimal grid placement sets any lot within two unit distance of the building. The answer for this case is 2.

1 0 1 2

2 1 2 1

1 0 1 0

2 1 2 1

"0" indicates optimal building placement and in this case the maximal value of all shortest distances to the closest building for each cell is "2".

Another such placement is:
2 1 0 1

2 1 1 1

1 0 1 0

2 1 2 1

https://youtu.be/HgTVjpgRTIk?t=3227 (problem definition using an example)

Solution:
1. Backtracking + BFS
Backtracking is used to explore the placement of the buildings, BFS is used to compute the distance of a building to the farthest empty lot (parking lot).

We use two approaches. They differ in the way backtracking is implemented.

Method 1:
First, we try every way to place the buildings on the grid using backtracking. We convert 1d index to row and column index of 2d matrix to place the building.
For each combination, we run a BFS to find the max distance from any empty cell to the nearest building. Among all placements, we keep track of the one that gives the smallest such distance.

Method 2:
First, we try every way to place the buildings on the grid using backtracking. We use the indices of the 2d matrix to perform backtracking. Once we place a building in cell (i,j), we increment the col index and start a new recursive call to place the next building in cell (i, j+1). If the col index exceeds the width, then we reset column index to 0 and increment the row index by 1 (i+1).
BFS to find min distance of is run as in method 1.

The BFS method to find the distance is common across both the methods. Using the 'mutate' flag, we show that we can compute the min distance by mutating the grid or by not mutating the grid. If we don't mutate the grid, we use an additional matrix visted[][] to keep track of the visited cells. If we mutate the grid, a cell containing a value of -1 is unvisited, 0 is where the building is placed, and a value > 0 is interpreted as the distance from nearest building. Mutating the grid helps to visualize where the buildings are placed in the optimal placement scenario and
the distances of the buildings from each non-occupied (non-building cells).
Notations (if grid is mutated)
  grid[x][y] == -1 (unvisited)
  grid[x][y] == 0  (ref cell)
  grid[x][y] == 1, 2 ... (distance from ref cell)

To visualize the grid, uncomment the line
mprint(dist_mat) in the base case (k==0) of recurse() function

https://youtu.be/HgTVjpgRTIk?t=3222

Time: O(C(H*W, N) * H*W)
(Note:
The time complexity is due to backtracking and BFS
Backtracking: C(HW, N) = HW choose N = no. of combinations of placing N buildings
BFS: H*W
Total Time: O(backtracking * BFS) = O(C(H*W, N) * HW)
Space: O(H*W) for the BFS queue and visited matrix (if mutated).

'''
from collections import deque
from copy import deepcopy as dcp
def mprint(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

def minDistance(grid, mutate):
    ''' find max distance from src cells to farthest cells using bfs; mutate    the grid if mutate=True
        Notations:
        grid[x][y] == -1 (unvisited)
        grid[x][y] == 0  (ref cell)
        grid[x][y] == 1, 2 ... (distance from ref cell)
    '''
    def bfs(grid, mutate=True):
        ''' bfs '''
        dirs = [[-1,0], [1,0], [0,-1], [0,1]] # U, D, L, R
        if not mutate:
            visited = [[False]*w for _ in range(h)]
        q = deque()
        for i in range(h):
            for j in range(w):
                if grid[i][j] == 0:
                    q.append((i,j))
                    if not mutate: visited[i][j] = True
        lvl = 0
        while q:
            sz = len(q)
            for _ in range(sz):
                curr = q.popleft()
                for dir in dirs:
                    x, y = curr[0] + dir[0] , curr[1] + dir[1]
                    # grid mutation
                    if mutate:
                        if 0<=x<=h-1 and 0<=y<=w-1 and grid[x][y] == -1:
                            q.append((x,y))
                            grid[x][y] = lvl + 1
                    else: # w/o grid mutation
                        if 0<=x<=h-1 and 0<=y<=w-1 and not visited[x][y]:
                            q.append((x,y))
                            visited[x][y] = True
            lvl += 1
        return lvl-1

    h =  len(grid)
    w = len(grid[0])
    dist = dcp(grid)
    lvl = bfs(dist, mutate=mutate)
    return lvl, dist

def optimalPlacement_1(w, h, n, mutate):
    def recurse(grid, start, k):
        nonlocal min_dist
        if k == 0:
            d, dist_mat = minDistance(grid, mutate=mutate)
            if d < min_dist:
                min_dist = d
                # print(grid)
                # print(f"\nmin distance = {d}")
                # mprint(dist_mat)
            return

        # logic
        # we number the cells in the grid using 1-dim notation
        # eg for a 4x3 grid, the 1-dim id of the cells are
        # 0 1 2 3
        # 4 5 6 7
        # 8 9 10 11
        # Then, vary 'start' from 0 ... 11 where 'start' is
        # first cell where we place a building
        for i in range(start, w*h):
            # convert 1-dim id to 2-dim dim id
            row = i // w
            col = i % w
            grid[row][col] = 0 # place a building in start
            recurse(grid, start+1, k-1) # place remaining buildings from start+1
            grid[row][col] = -1
        return

    grid = [[-1]*w for _ in range(h)]
    min_dist = float('inf')
    start = 0
    recurse(grid, start, n)
    return min_dist

def optimalPlacement_2(w, h, n, mutate):
    def recurse(grid, row, col, k):
        nonlocal min_dist
        if k == 0:
            d, dist_mat = minDistance(grid, mutate=mutate)
            if d < min_dist:
                min_dist = d
                # print(grid)
                # print(f"\nmin distance = {d}")
                # mprint(dist_mat)
            return

        if col == w:
           row += 1
           col = 0

        # logic
        for i in range(row, h):
            for j in range(col, w):
                grid[i][j] = 0
                recurse(grid, i, j+1, k-1)
                grid[i][j] = -1
            col = 0
        return

    grid = [[-1]*w for _ in range(h)]
    min_dist = float('inf')
    recurse(grid, 0, 0, n)
    return min_dist

def run_optimalPlacement():
    tests = [(5, 4, 2, 3),
             (4, 4, 3, 2),
             (5, 4, 6, 1),
    ]
    for test in tests:
        w, h, n, ans = test[0], test[1], test[2], test[3]
        print(f"\nWidth = {w}, Height = {h}")
        print(f"Num buildings to place = {n}")
        for method in [1, 2]:
            for mutate in [True, False]:
                if method == 1:
                    dist = optimalPlacement_1(w, h, n, mutate)
                elif method == 2:
                    dist = optimalPlacement_2(w, h, n, mutate)
                print(f"distance = {dist} (Method: {method}; Mutate: {mutate}")
                success = (ans == dist)
                print(f"Pass: {success}")
                if not success:
                    print(f"Failed")
                    return

run_optimalPlacement()

# # w, h, n, ans = 5, 4, 2, 3
# w, h, n, ans = 5, 4, 6, 1
# dist = optimalPlacement_2(w, h, n, True)
# print("Done")

# w, h, n, ans = 4, 4, 3, 2
# dist = optimalPlacement_2(w, h, n, False)
# print("Done")
