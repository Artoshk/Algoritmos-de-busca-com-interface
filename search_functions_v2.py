import random
import sys
from matplotlib import pyplot as plt
import networkx as nx

# Set the animation speed
DELAY: float = 0.1

def draw_path(path: list[str], graph: nx.Graph, draw):
    for node in path:
        graph.nodes[node]['color'] = 'orange'
        #also change the color of the edges
        if node != path[0]:
            graph.edges[(node, path[path.index(node) - 1])]['color'] = 'orange'
        draw(graph)

# Breadth-First Search algorithm
def flooding(graph: nx.Graph, start_node: str, resource: str, draw, cache: dict = None, max_ttl: int = sys.maxsize):
    visited = set()
    queue = [(start_node, 0, [start_node])]  # Add path information to the queue
    path = []
    cache_enabled: bool = True if cache is not None else False

    if cache_enabled:
        cache_key = (start_node, resource)
        if cache_key in cache:
            print("CACHE HIT!")
            draw_path(cache[cache_key], graph, draw)
            return cache[cache_key], 1
    
    while queue:
        node, ttl, current_path = queue.pop(0)  # Get the current path
        visited.add(node)
        
        if ttl >= max_ttl:
            break
        
        if 'color' in graph.nodes[node] and graph.nodes[node]['color'] != 'lightgreen':
            graph.nodes[node]['color'] = 'lightgreen'
            draw(graph)
            plt.pause(DELAY)
        
        if resource in graph.nodes[node].get('resources', []):
            if path == []:
                path = current_path  # Update the path
                draw_path(path, graph, draw)
                if cache_enabled:
                    cache[cache_key] = path

        # just to keeps the path orange
        if path != []:
            draw_path(path, graph, draw)
        
        neighbors = graph.neighbors(node)
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append((neighbor, ttl + 1, current_path + [neighbor]))  # Update the path for each neighbor
                if 'color' in graph.edges[(node, neighbor)] and graph.edges[(node, neighbor)]['color'] != 'red':
                    graph.edges[(node, neighbor)]['color'] = 'red'
                    draw(graph)
                    plt.pause(DELAY)
                if 'color' in graph.nodes[neighbor] and graph.nodes[neighbor]['color'] != 'yellow':
                    graph.nodes[neighbor]['color'] = 'yellow'
                    draw(graph)
                    plt.pause(DELAY)
    
    return path, len(visited)  # Return the path and the number of visited nodes


def random_walk(graph: nx.Graph, start_node: str, resource: str, draw, cache: dict = None, max_ttl: int = sys.maxsize):
    visited = set()
    path = [start_node]
    cache_enabled: bool = True if cache is not None else False
    connection_count = 0

    if cache_enabled:
        cache_key = (start_node, resource)
        if cache_key in cache:
            print("CACHE HIT!")
            draw_path(cache[cache_key], graph, draw)
            return cache[cache_key], 1
    
    node = start_node
    while True:
        visited.add(node)

        if 'color' in graph.nodes[node] and graph.nodes[node]['color'] != 'lightgreen':
            graph.nodes[node]['color'] = 'lightgreen'
            draw(graph)
            plt.pause(DELAY)
        
        if resource in graph.nodes[node].get('resources', []):
            draw_path(path, graph, draw)
            if cache_enabled:
                cache[cache_key] = path
            break
        
        connection_count += 1
        if connection_count >= max_ttl:
            break

        neighbors = list(graph.neighbors(node))
        random.shuffle(neighbors)
        next_node = None
        for neighbor in neighbors:
            if neighbor not in visited:
                next_node = neighbor
                break
        
        if next_node is None:
            # Backtrack to the previous node
            if len(path) > 1:
                path.pop()
                node = path[-1]
            else:
                break

        if next_node is not None:
            if 'color' in graph.edges[(node, next_node)] and graph.edges[(node, next_node)]['color'] != 'red':
                graph.edges[(node, next_node)]['color'] = 'red'
                draw(graph)
                plt.pause(DELAY)
            if 'color' in graph.nodes[next_node] and graph.nodes[next_node]['color'] != 'yellow':
                graph.nodes[next_node]['color'] = 'yellow'
                draw(graph)
                plt.pause(DELAY)
            
            path.append(next_node)  # Update the path
            node = next_node
    
    return path, len(visited)  # Return the path and the number of visited nodes