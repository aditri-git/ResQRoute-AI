import streamlit as st
st.caption(
    "ResQRoute AI | Educational pathfinding simulation | "
    "Not intended for real-world emergency dispatch."
)
import heapq
from collections import deque


def bfs(start, goal, rows, cols, obstacles):

    # Step 1: Create a queue and insert starting position
    queue = deque([start])

    # Step 2: Store the parent of each visited position
    parent = {start: None}

    explored = 0

    # Step 3: Continue until queue becomes empty
    while queue:

        # Remove the first position from queue
        current = queue.popleft()

        explored += 1

        # Check whether destination is reached
        if current == goal:

            path = []
            node = goal

            while node is not None:
                path.append(node)
                node = parent[node]

            return path[::-1], explored

        r, c = current

        # Four possible movements
        moves = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]

        for dr, dc in moves:

            nr = r + dr
            nc = c + dc

            neighbor = (nr, nc)

            # Check grid boundaries and obstacles
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and neighbor not in obstacles
                and neighbor not in parent
            ):

                parent[neighbor] = current
                queue.append(neighbor)

    # No route exists
    return [], explored


# DFS - Depth First Search

def dfs(start, goal, rows, cols, obstacles):

    # Step 1: Create a stack
    stack = [start]

    # Step 2: Store parent positions
    parent = {start: None}

    explored = 0

    # Step 3: Continue until stack is empty
    while stack:

        # Remove the last inserted position
        current = stack.pop()

        explored += 1

        # Check if destination is reached
        if current == goal:

            path = []
            node = goal

            while node is not None:
                path.append(node)
                node = parent[node]

            return path[::-1], explored

        r, c = current

        # Four possible movements
        moves = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]

        for dr, dc in moves:

            nr = r + dr
            nc = c + dc

            neighbor = (nr, nc)

            # Check boundaries and obstacles
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and neighbor not in obstacles
                and neighbor not in parent
            ):

                parent[neighbor] = current
                stack.append(neighbor)

    # No route found
    return [], explored



# Manhattan Distance Heuristic

def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Calculate movement cost

def movement_cost(position, danger_zones):

    if position in danger_zones:
        return 5

    return 1


# A* Search Algorithm

def astar(start, goal, rows, cols, obstacles, danger_zones):

    counter = 0

    # Priority queue
    open_list = [
        (heuristic(start, goal), counter, start)
    ]

    parent = {start: None}

    g_score = {start: 0}

    explored = 0

    closed = set()

    while open_list:

        f_score, _, current = heapq.heappop(open_list)

        if current in closed:
            continue

        closed.add(current)
        explored += 1

        # Check destination
        if current == goal:

            path = []
            node = goal

            while node is not None:
                path.append(node)
                node = parent[node]

            return path[::-1], explored

        r, c = current

        moves = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dr, dc in moves:

            nr = r + dr
            nc = c + dc

            neighbor = (nr, nc)

            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and neighbor not in obstacles
                and neighbor not in closed
            ):

                tentative_g = (
                    g_score[current]
                    + movement_cost(neighbor, danger_zones)
                )

                if tentative_g < g_score.get(
                    neighbor, float("inf")
                ):

                    parent[neighbor] = current

                    g_score[neighbor] = tentative_g

                    f = (
                        tentative_g
                        + heuristic(neighbor, goal)
                    )

                    counter += 1

                    heapq.heappush(
                        open_list,
                        (f, counter, neighbor)
                    )

    return [], explored


# Calculate total path cost

def calculate_cost(path, danger_zones):

    if not path:
        return 0

    total = 0

    for position in path[1:]:

        total += movement_cost(position, danger_zones)

    return total




