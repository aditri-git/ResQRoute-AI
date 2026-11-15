
import streamlit as st
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from algorithms.search import bfs, dfs, astar, calculate_cost


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="ResQRoute AI",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 ResQRoute AI")
st.subheader("Intelligent Rescue Navigator")

st.write(
    "An AI-based pathfinding system that helps identify "
    "routes from a rescue team's location to a victim."
)

st.info(
    "Educational simulation only. This application does "
    "not provide real emergency dispatch or rescue guidance."
)

# ---------------- GRID SETTINGS ----------------

ROWS = 12
COLS = 12

# ---------------- SIDEBAR INPUTS ----------------

st.sidebar.header("Rescue Environment")

start_row = st.sidebar.number_input(
    "Rescue Team Row", 0, ROWS - 1, 0
)
start_col = st.sidebar.number_input(
    "Rescue Team Column", 0, COLS - 1, 0
)

goal_row = st.sidebar.number_input(
    "Victim Row", 0, ROWS - 1, 11
)
goal_col = st.sidebar.number_input(
    "Victim Column", 0, COLS - 1, 11
)

st.sidebar.markdown("---")

st.sidebar.write("Enter coordinates as row,column")
st.sidebar.caption("Separate multiple coordinates using semicolons.")


# ---------------- RANDOM ENVIRONMENT GENERATOR ----------------


def generate_environment():
    start = (0, 0)
    goal = (11, 11)

    # Try generating different environments
    for attempt in range(100):

        available_cells = [
            (r, c)
            for r in range(ROWS)
            for c in range(COLS)
            if (r, c) != start and (r, c) != goal
        ]

        random.shuffle(available_cells)

        obstacles = set(available_cells[:18])
        danger_zones = set(available_cells[18:28])

        # Check whether a rescue route exists
        path, explored = bfs(
            start,
            goal,
            ROWS,
            COLS,
            obstacles
        )

        if path:
            return obstacles, danger_zones

    # Fallback: an empty environment always has a route
    return set(), set()

    start = (0, 0)
    goal = (11, 11)

    available_cells = [
        (r, c)
        for r in range(ROWS)
        for c in range(COLS)
        if (r, c) != start and (r, c) != goal
    ]

    random.shuffle(available_cells)

    obstacles = set(available_cells[:18])
    danger_zones = set(available_cells[18:28])

    return obstacles, danger_zones


def generate_random_map():
    obstacles, danger_zones = generate_environment()

    st.session_state["obstacle_input"] = "; ".join(
        f"{r},{c}" for r, c in sorted(obstacles)
    )

    st.session_state["danger_input"] = "; ".join(
        f"{r},{c}" for r, c in sorted(danger_zones)
    )


# Initialize widget values before displaying them
if "obstacle_input" not in st.session_state:
    st.session_state["obstacle_input"] = "2,2; 2,3; 2,4; 5,5; 6,5"

if "danger_input" not in st.session_state:
    st.session_state["danger_input"] = "4,4; 4,5; 7,7"


st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Environment Generator")

st.sidebar.button(
    "🎲 Generate Random Environment",
    on_click=generate_random_map
)

obstacle_input = st.sidebar.text_input(
    "Obstacle Coordinates",
    key="obstacle_input"
)

danger_input = st.sidebar.text_input(
    "Danger Zone Coordinates",
    key="danger_input"
)


algorithm = st.sidebar.selectbox(
    "Choose Search Algorithm",
    ["BFS", "DFS", "A*"]
)

# ---------------- COORDINATE PROCESSING ----------------

def parse_coordinates(text):
    coordinates = set()

    if not text.strip():
        return coordinates

    for item in text.split(";"):
        parts = item.strip().split(",")

        if len(parts) != 2:
            raise ValueError(
                "Use row,column format, e.g. 2,3"
            )

        row = int(parts[0].strip())
        col = int(parts[1].strip())

        if not (0 <= row < ROWS and 0 <= col < COLS):
            raise ValueError(
                f"Coordinate {row},{col} is outside the grid."
            )

        coordinates.add((row, col))

    return coordinates


# ---------------- RUN SEARCH ----------------

if st.button("🚑 Find Rescue Route", type="primary"):

    try:
        start = (int(start_row), int(start_col))
        goal = (int(goal_row), int(goal_col))

        obstacles = parse_coordinates(obstacle_input)
        danger_zones = parse_coordinates(danger_input)

        if start == goal:
            st.error("Start and victim locations must be different.")

        elif start in obstacles or goal in obstacles:
            st.error("Start or victim location cannot be an obstacle.")

        elif start in danger_zones or goal in danger_zones:
            st.error("Keep start and victim locations outside danger zones.")

        elif obstacles & danger_zones:
            st.error("A cell cannot be both an obstacle and a danger zone.")

        else:
            # Select algorithm
            if algorithm == "BFS":
                path, explored = bfs(
                    start, goal, ROWS, COLS, obstacles
                )

            elif algorithm == "DFS":
                path, explored = dfs(
                    start, goal, ROWS, COLS, obstacles
                )

            else:
                path, explored = astar(
                    start, goal, ROWS, COLS,
                    obstacles, danger_zones
                )

            # Display results
            if not path:
                st.error("No rescue route could be found.")

            else:
                st.success("Rescue route successfully calculated!")

                travel_cost = calculate_cost(
                    path, danger_zones
                )

                col1, col2, col3 = st.columns(3)

                col1.metric("Algorithm", algorithm)
                col2.metric("Cells Explored", explored)
                col3.metric("Route Cost", travel_cost)

                st.write("**Calculated Route:**")
                st.code(" → ".join(map(str, path)))

                st.write(
                    f"**Number of movements:** {len(path) - 1}"
                )

                # ---------------- DRAW GRID ----------------

                grid = [
                    [0 for _ in range(COLS)]
                    for _ in range(ROWS)
                ]

                for cell in obstacles:
                    grid[cell[0]][cell[1]] = 1

                for cell in danger_zones:
                    grid[cell[0]][cell[1]] = 2

                for r, c in path:
                    grid[r][c] = 3

                grid[start[0]][start[1]] = 4
                grid[goal[0]][goal[1]] = 5

                cmap = ListedColormap([
                    "white",
                    "black",
                    "orange",
                    "lightgreen",
                    "blue",
                    "red"
                ])

                fig, ax = plt.subplots(figsize=(9, 8))

                ax.imshow(
                    grid,
                    cmap=cmap,
                    vmin=0,
                    vmax=5
                )

                ax.set_xticks(range(COLS))
                ax.set_yticks(range(ROWS))
                ax.set_xticklabels(range(COLS))
                ax.set_yticklabels(range(ROWS))

                ax.set_xticks(
                    [x - 0.5 for x in range(1, COLS)],
                    minor=True
                )
                ax.set_yticks(
                    [y - 0.5 for y in range(1, ROWS)],
                    minor=True
                )

                ax.grid(
                    which="minor",
                    color="gray",
                    linewidth=0.7
                )

                ax.set_title("ResQRoute AI - Rescue Map")

                ax.set_xlabel("Column")
                ax.set_ylabel("Row")

                st.pyplot(fig)
                plt.close(fig)

                st.markdown("""
                **Map Legend**

                - 🔵 Blue: Rescue team
                - 🔴 Red: Victim
                - ⬛ Black: Obstacle
                - 🟠 Orange: Danger zone
                - 🟩 Light green: Calculated route
                - ⬜ White: Free space
                """)

    except ValueError as error:
        st.error(f"Invalid input: {error}")


# ---------------- COMPARE ALL ALGORITHMS ----------------

st.markdown("---")
st.header("📊 Compare All Algorithms")

st.write(
    "Run BFS, DFS and A* on the same rescue environment "
    "to compare their performance."
)

if st.button("Compare All Algorithms"):

    try:
        start = (int(start_row), int(start_col))
        goal = (int(goal_row), int(goal_col))

        obstacles = parse_coordinates(obstacle_input)
        danger_zones = parse_coordinates(danger_input)

        if start == goal:
            st.error("Start and victim locations must be different.")

        elif start in obstacles or goal in obstacles:
            st.error("Start or victim cannot be an obstacle.")

        elif start in danger_zones or goal in danger_zones:
            st.error("Start and victim must be outside danger zones.")

        elif obstacles & danger_zones:
            st.error("A cell cannot be both obstacle and danger zone.")

        else:
            # Run all three algorithms
            bfs_path, bfs_explored = bfs(
                start, goal, ROWS, COLS, obstacles
            )

            dfs_path, dfs_explored = dfs(
                start, goal, ROWS, COLS, obstacles
            )

            astar_path, astar_explored = astar(
                start, goal, ROWS, COLS,
                obstacles, danger_zones
            )

            # Prepare comparison results
            results = []

            algorithms = [
                ("BFS", bfs_path, bfs_explored),
                ("DFS", dfs_path, dfs_explored),
                ("A*", astar_path, astar_explored)
            ]

            for name, path, explored in algorithms:
                results.append({
                    "Algorithm": name,
                    "Route Found": "Yes" if path else "No",
                    "Movements": len(path) - 1 if path else "N/A",
                    "Explored Cells": explored,
                    "Travel Cost": (
                        calculate_cost(path, danger_zones)
                        if path else "N/A"
                    )
                })

            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True
            )

            st.success("Algorithm comparison completed!")

            st.markdown("""
            **How to interpret the comparison:**

            - **BFS:** Finds a route with the minimum number of steps.
            - **DFS:** May find a route with more steps.
            - **A*:** Uses path cost and Manhattan distance to select
              a low-cost route.
            - **Explored Cells:** Number of cells visited by the
              algorithm before finding the goal.
            """)

    except ValueError as error:
        st.error(f"Invalid input: {error}")

st.markdown("---")
st.caption("ResQRoute AI | AI Search Algorithms Project")
