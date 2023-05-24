from matplotlib.axes import Axes
from matplotlib.figure import Figure
import networkx as nx
import matplotlib.pyplot as plt
import random

# Create an empty graph
G: nx.Graph = nx.Graph()

# Add nodes to the graph
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Add edges to the graph
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10)])

# Define the layout for visualization
pos: dict = nx.spring_layout(G)

# Set the animation speed
DELAY: float = 0.8

# Build the plot
fig: Figure
ax: Axes
fig, ax = plt.subplots(figsize=(8, 6))

# Function to update the visualization
def update(node: int, path: list[int]):
    ax.clear()

    # Customize the visualization here, e.g., node colors, labels, edge styles
    node_colors = ['lightblue' if n != node else 'red' for n in G.nodes()]
    nx.draw(G, pos=pos, with_labels=True, node_color=node_colors, node_size=800, font_weight='bold', ax=ax)

    # Highlight the path
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, edge_color='red', width=2.0, ax=ax)

    # Customize other visual elements, titles, etc.

# Call the update function to display the initial graph
update(None, [])

# Breadth-First Search algorithm
def bfs(graph: nx.Graph, start_node: int, end_node: int) -> list[int]:
    visited = set()
    queue = [(start_node, [start_node])]

    while queue:
        current_node, path = queue.pop(0)
        visited.add(current_node)

        # Visualization step
        update(current_node, path)
        plt.pause(DELAY)  # Pause to visualize each step

        if current_node == end_node:
            return path

        for neighbor in graph[current_node]:
            if neighbor not in visited and neighbor not in [node for node, _ in queue]:
                queue.append((neighbor, path + [neighbor]))

    return None

def dfs(graph: nx.Graph, start_node: int, end_node: int) -> list[int]:
    visited = set()
    stack = [(start_node, [start_node])]

    while stack:
        current_node, path = stack.pop()

        if current_node == end_node:
            update(current_node, path)
            return path
        
        if current_node not in visited:
            visited.add(current_node)
            # Visualization step
            update(current_node, path)
            plt.pause(DELAY)  # Pause to visualize each step

            neighbors = graph[current_node]
            unvisited_neighbors = [n for n in neighbors if n not in visited]
            for neighbor in reversed(unvisited_neighbors):
                stack.append((neighbor, path + [neighbor]))

    return None

import random

def random_dfs(graph: nx.Graph, start_node: int, end_node: int) -> list[int]:
    visited = set()
    stack = [(start_node, [start_node])]

    while stack:
        current_node, path = stack.pop()

        if current_node == end_node:
            update(current_node, path)
            return path

        if current_node not in visited:
            visited.add(current_node)
            # Visualization step
            update(current_node, path)
            plt.pause(DELAY)  # Pause to visualize each step

            neighbors = graph[current_node]
            unvisited_neighbors = [n for n in neighbors if n not in visited]
            random.shuffle(unvisited_neighbors)  # Shuffle the unvisited neighbors
            for neighbor in reversed(unvisited_neighbors):
                stack.append((neighbor, path + [neighbor]))

    return None


# Define start and end nodes
start_node: int = 1  # Replace with your preferred start node
end_node: int = 5  # Replace with your preferred end node

# Run BFS and DFS from the start node
print("Running BFS from node", start_node, "to node", end_node)
bfs_path = bfs(G, start_node, end_node)
print("BFS Path:", bfs_path)

plt.pause(2)  # Pause for 2 seconds between BFS and DFS

print("Running DFS from node", start_node, "to node", end_node)
dfs_path = dfs(G, start_node, end_node)
print("DFS Path:", dfs_path)

plt.pause(2)  # Pause for 2 seconds between DFS and Random DFS

print("Running Random DFS from node", start_node, "to node", end_node)
random_dfs_path = random_dfs(G, start_node, end_node)
print("Random DFS Path:", random_dfs_path)

plt.show()
