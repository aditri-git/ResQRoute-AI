
from algorithms.search import bfs, dfs, astar, calculate_cost

# Define the rescue environment
start = (0, 0)
goal = (4, 4)

obstacles = {
    (1, 0),
    (1, 1),
    (1, 2)
}

danger_zones = {
    (2, 3),
    (3, 3)
}

rows = 5
cols = 5

# Test BFS
print("\n----- BFS RESULT -----")
bfs_path, bfs_explored = bfs(
    start, goal, rows, cols, obstacles
)
print("Path:", bfs_path)
print("Explored cells:", bfs_explored)

# Test DFS
print("\n----- DFS RESULT -----")
dfs_path, dfs_explored = dfs(
    start, goal, rows, cols, obstacles
)
print("Path:", dfs_path)
print("Explored cells:", dfs_explored)

# Test A*
print("\n----- A* RESULT -----")
astar_path, astar_explored = astar(
    start, goal, rows, cols, obstacles, danger_zones
)
print("Path:", astar_path)
print("Explored cells:", astar_explored)

if astar_path:
    print("Number of steps:", len(astar_path) - 1)
    print("Total travel cost:", calculate_cost(
        astar_path, danger_zones
    ))
else:
    print("No rescue route found.")



