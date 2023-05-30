from matplotlib.axes import Axes
from matplotlib.figure import Figure
import networkx as nx
import matplotlib.pyplot as plt
from search_functions import flooding, random_walk
from validate import read_and_validate_network

G = read_and_validate_network("C:/Users/ander/OneDrive/Desktop/Algoritmos-de-busca-com-interface/grafo.txt")
cache_dfs = {}
cache_bfs = {}

# Define the layout for visualization
pos: dict = nx.spring_layout(G)

# Build the plot
fig: Figure
ax: Axes
fig, ax = plt.subplots(figsize=(8, 6))

# Function to update the visualization
def update(node: int, path: list[int], color: str = 'red'):
    ax.clear()

    # Customize the visualization here, e.g., node colors, labels, edge styles
    node_colors = ['lightblue' if n != node else color for n in G.nodes()]
    nx.draw(G, pos=pos, with_labels=True, node_color=node_colors, node_size=800, font_weight='bold', ax=ax)

    # Highlight the path
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, edge_color= color, width=2.0, ax=ax)

    # Draw the resources
    for node in G.nodes():
        # if node in path: # Only draw the resources for the nodes in the path
        if 'resources' in G.nodes[node]:
            resources = G.nodes[node]['resources']
            ax.text(pos[node][0], pos[node][1] + 0.15, resources, horizontalalignment='center', verticalalignment='center')


# Call the update function to display the initial graph
update(None, [])


# Define start and resource to search
start_node: str = 'n1'  # Replace with your preferred start node
resource: str = 'r15'  # Replace with your preferred end node
plt.pause(2)

print("Running Flooding from node", start_node, "to resource", resource)
flooding_path_cache, ttl = flooding(G, start_node, resource, update, cache_bfs)
print("ttl:", ttl)
print("Flooding Path:", flooding_path_cache, "\n")
plt.pause(2)

print("Running Random Walk from node", start_node, "to resource", resource)
random_walk_path, ttl = random_walk(G, start_node, resource, update, cache_dfs)
print("ttl:", ttl)
print("Random Walk Path:", random_walk_path, "\n")
plt.pause(2)  

print("Running Flooding from node", start_node, "to resource", resource)
flooding_path_cache, ttl = flooding(G, start_node, resource, update, cache_bfs)
print("ttl:", ttl)
print("Flooding Path:", flooding_path_cache, "\n")
plt.pause(2)

print("Running Random Walk from node", start_node, "to resource", resource)
random_walk_path, ttl = random_walk(G, start_node, resource, update, cache_dfs)
print("ttl:", ttl)
print("Random Walk Path:", random_walk_path, "\n")

plt.show()
