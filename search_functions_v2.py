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
    connection_count = 0

    if cache_enabled:
        cache_key = (start_node, resource)
        if cache_key in cache:
            print("CACHE HIT! Break")
            graph.nodes[cache[cache_key][-1]]['color'] = 'red'
            draw(graph)
            return cache[cache_key], 0
    
    while queue:
        node, ttl, current_path = queue.pop(0)  # Get the current path
        visited.add(node)
        # TO DO: ver isso
        connection_count += 1
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
                
                if cache_enabled:
                    cache_key_neighbor = (neighbor, resource)
                    if cache_key_neighbor in cache:
                        print("CACHE HIT!")
                        graph.nodes[cache[cache_key_neighbor][-1]]['color'] = 'red'
                        combined_path = current_path + cache[cache_key_neighbor]
                        combined_path = list(dict.fromkeys(combined_path))
                        draw(graph)
                        cache[cache_key] = combined_path
                        return combined_path, connection_count

            connection_count += 1
    
    return path, connection_count  # Return the path and the number of visited nodes


def random_walk(graph: nx.Graph, start_node: str, resource: str, draw, cache: dict = None, max_ttl: int = sys.maxsize):
    visited = set()
    path = [start_node]
    cache_enabled: bool = True if cache is not None else False
    connection_count = 0

    if cache_enabled:
        cache_key = (start_node, resource)
        if cache_key in cache:
            graph.nodes[cache[cache_key][-1]]['color'] = 'orange'
            draw(graph)
            return cache[cache_key], 0
    
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
        
            if cache_enabled:
                cache_key_neighbor = (next_node, resource)
                if cache_key_neighbor in cache:
                    graph.nodes[cache[cache_key_neighbor][-1]]['color'] = 'orange'
                    combined_path = path + cache[cache_key_neighbor]
                    combined_path = list(dict.fromkeys(combined_path))
                    draw(graph)
                    return combined_path, connection_count


    return path, len(visited)  # Return the path and the number of visited nodes



def instant_random_walk(graph: nx.Graph, start_node: str, resource: str, cache: dict = None, max_ttl: int = sys.maxsize):
    visited = set()
    path = [start_node]
    cache_enabled: bool = True if cache is not None else False
    connection_count = 0

    if cache_enabled:
        cache_key = (start_node, resource)
        if cache_key in cache:
            graph.nodes[cache[cache_key][-1]]['color'] = 'orange'
            return cache[cache_key], 0
    
    node = start_node
    while True:
        visited.add(node)

        if 'color' in graph.nodes[node] and graph.nodes[node]['color'] != 'lightgreen':
            graph.nodes[node]['color'] = 'lightgreen'
        
        if resource in graph.nodes[node].get('resources', []):
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
            if 'color' in graph.nodes[next_node] and graph.nodes[next_node]['color'] != 'yellow':
                graph.nodes[next_node]['color'] = 'yellow'
            
            path.append(next_node)  # Update the path
            node = next_node
        
            if cache_enabled:
                cache_key_neighbor = (next_node, resource)
                if cache_key_neighbor in cache:
                    graph.nodes[cache[cache_key_neighbor][-1]]['color'] = 'orange'
                    combined_path = path + cache[cache_key_neighbor]
                    combined_path = list(dict.fromkeys(combined_path))
                    return combined_path, connection_count


    return path, len(visited)  # Return the path and the number of visited nodes