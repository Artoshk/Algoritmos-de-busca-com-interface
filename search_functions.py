import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
from typing import Callable

# Set the animation speed
DELAY: float = 0.8

# Breadth-First Search algorithm
def flooding(graph: nx.Graph, start_node: str, resource: str, update: Callable[[str, list[str], str], None], cache: dict = None, max_ttl: int = sys.maxsize):
    connection_count = 0
    cache_enabled: bool = True if cache is not None else False
    return_val = None

    if cache_enabled:
        cache_key = (start_node, resource)
        if cache_key in cache:
            print("CACHE HIT!")
            connection_count += 1
            update(cache[cache_key][-1], cache[cache_key], 'green')
            return cache[cache_key], connection_count

    visited = set()
    queue = [(start_node, [start_node])]

    while queue:
        current_node, path = queue.pop(0)
        visited.add(current_node)

        connection_count += 1
        update(current_node, path)
        plt.pause(DELAY)

        if resource in graph.nodes[current_node].get('resources', []):
            if cache_enabled:
                cache[cache_key] = path

            return_val = path
            update(current_node, path, 'orange')
            plt.pause(DELAY)

        if connection_count >= max_ttl:
            return None, connection_count

        for neighbor in graph[current_node]:
            if neighbor not in visited and neighbor not in [node for node, _ in queue]:
                queue.append((neighbor, path + [neighbor]))

        # if len(path) > depth:  # Check if the current path depth is greater than the previous depth
        #     continue
            
    return return_val, connection_count


# Random Depth-First Search algorithm
def random_walk(graph: nx.Graph, start_node: str, resource: str, update: Callable[[str, list[str], str], None], cache: dict = None, max_ttl: int = sys.maxsize):
    connection_count = 0
    cache_enabled: bool = True if cache is not None else False

    if cache_enabled:
        cache_key = (start_node, resource)
        if cache_key in cache:
            print("CACHE HIT!")
            connection_count += 1
            update(cache[cache_key][-1], cache[cache_key], color='green')
            return cache[cache_key], connection_count

    visited = set()
    stack = [(start_node, [start_node])]

    while stack:
        current_node, path = stack.pop()
        connection_count += 1

        if connection_count >= max_ttl:
            return None, connection_count

        if resource in graph.nodes[current_node].get('resources', []):
            update(current_node, path)
            if cache_enabled:
                cache[cache_key] = path
            return path, connection_count

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

    return None, connection_count