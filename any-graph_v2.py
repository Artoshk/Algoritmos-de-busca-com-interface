from matplotlib.axes import Axes
import networkx as nx
import matplotlib.pyplot as plt
from search_functions_v2 import flooding, random_walk, instant_random_walk
from validate import read_and_validate_network

G = read_and_validate_network("grafo.txt")
cache_dfs = {}
cache_bfs = {}

# Define the layout for visualization
pos: dict = nx.spring_layout(G)

#for each node in G.nodes() add a color parameter
for node in G.nodes():
    if 'color' not in G.nodes[node]:
        G.nodes[node]['color'] = 'lightblue'

# for each edge in G.edges() add a color parameter
for edge in G.edges():
    if 'color' not in G.edges[edge]:
        G.edges[edge]['color'] = 'black'

ax: Axes
_, ax = plt.subplots(figsize=(8, 6))

def draw(G: nx.Graph):
    ax.clear()
    
    # Customize the visualization here, e.g., node colors, labels, edge styles
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    edge_colors = [G.edges[edge]['color'] for edge in G.edges()]
    nx.draw(G, pos=pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=800, font_weight='bold', ax=ax)

    # Draw the resources
    for node in G.nodes():
        # if node in path: # Only draw the resources for the nodes in the path
        if 'resources' in G.nodes[node]:
            resources = G.nodes[node]['resources']
            ax.text(pos[node][0], pos[node][1] + 0.15, resources, horizontalalignment='center', verticalalignment='center')

def clear(G: nx.Graph):
    for node in G.nodes():
        if 'color' in G.nodes[node]:
            G.nodes[node]['color'] = 'lightblue'
    for edge in G.edges():
        if 'color' in G.edges[edge]:
            G.edges[edge]['color'] = 'black'
    draw(G)

# Call the update function to display the initial graph
draw(G)

# Define start and resource to search
start_node: str = 'n1'  # Replace with your preferred start node
resource: str = 'r15'  # Replace with your preferred end node
plt.pause(2)

# print("Running Flooding from node", start_node, "to resource", resource)
# connection_count = flooding(G, 'n2', resource, draw, cache_bfs)
# print("connection_count:", connection_count)

# plt.pause(5)
# clear(G)

# print("Running Flooding from node", start_node, "to resource", resource)
# connection_count = flooding(G, start_node, resource, draw, cache_bfs)
# print("connection_count:", connection_count)

# plt.pause(5)
# clear(G)

# print("Running Flooding from node", start_node, "to resource", resource)
# connection_count = flooding(G, 'n3', resource, draw, cache_bfs)
# print("connection_count:", connection_count)

# plt.pause(5)
# clear(G)

# print("Running Flooding from node", start_node, "to resource", resource)
# connection_count = flooding(G, start_node, resource, draw, cache_bfs)
# print("connection_count:", connection_count)

# plt.pause(5)
# clear(G)



# print("Running Random Walk from node", start_node, "to resource", resource)
# connection_count = random_walk(G, 'n2', resource, draw, cache_dfs)
# print("connection_count:", connection_count)

# plt.pause(5)
# clear(G)

# print("Running Random Walk from node", start_node, "to resource", resource)
# connection_count = random_walk(G, start_node, resource, draw, cache_dfs)
# print("connection_count:", connection_count)

# plt.pause(5)
# clear(G)

values = []
for _ in range(1000):
    path, connection_count = instant_random_walk(G, start_node, resource)
    values.append(connection_count)
    clear(G)

# min, max, mean, median, std, 99 percentile, 99.9 percentile
min = min(values)
max = max(values)
mean = sum(values) / len(values)
median = sorted(values)[len(values) // 2]
std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5

print("min:", min)
print("max:", max)
print("mean:", mean)
print("median:", median)
print("std:", std)

plt.show()
