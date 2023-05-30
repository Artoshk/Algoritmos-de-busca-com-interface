import re
import networkx as nx

def parse_resources(line):
    match = re.match(r'\s*(\S+)\s*:\s*(.*)', line)
    if match:
        node = match.group(1)
        resources = [res.strip() for res in match.group(2).split(',')]
        return node, resources
    return None, None

def parse_edges(line):
    match = re.match(r'\s*(\S+),\s*(\S+)', line)
    if match:
        return match.group(1), match.group(2)
    return None, None

def validate_graph(input_file):
    num_nodes = None
    min_neighbors = None
    max_neighbors = None
    resources = {}
    edges = []
    
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('num_nodes:'):
                match = re.match(r'num_nodes:\s*(\d+)', line)
                if match:
                    num_nodes = int(match.group(1))
            elif line.startswith('min_neighbors:'):
                match = re.match(r'min_neighbors:\s*(\d+)', line)
                if match:
                    min_neighbors = int(match.group(1))
            elif line.startswith('max_neighbors:'):
                match = re.match(r'max_neighbors:\s*(\d+)', line)
                if match:
                    max_neighbors = int(match.group(1))
            elif line == 'resources:':
                for line in file:
                    line = line.strip()
                    if line == 'edges:':
                        break
                    node, node_resources = parse_resources(line)
                    if node and node_resources:
                        resources[node] = node_resources
            else:
                node1, node2 = parse_edges(line)
                if node1 and node2:
                    edges.append((node1, node2))

    if num_nodes is None or min_neighbors is None or max_neighbors is None:
        return False, "Invalid parameters"
    
    # Check for nodes without resources (optional)
    # if len(resources) != num_nodes:
    #     return False, "Nodes without resources"
    
    if min_neighbors < 0 or max_neighbors < 0 or min_neighbors > max_neighbors:
        return False, "Invalid neighbor limits"
    
    if len(edges) == 0:
        return False, "No edges found"
    
    # Check for self loops
    for edge in edges:
        if edge[0] == edge[1]:
            return False, "Self loops are not allowed"
    
    # Check for invalid number of neighbors
    node_counts = {}
    for edge in edges:
        for node in edge:
            if node in node_counts:
                node_counts[node] += 1
            else:
                node_counts[node] = 1

    valid = True
    for node, count in node_counts.items():
        if count < min_neighbors or count > max_neighbors:
            valid = False
            break

    if not valid:
        return False, "Invalid number of neighbors"

    graph = nx.Graph()
    graph.add_edges_from(edges)
    
    # Check for partitioned graph
    if not nx.is_connected(graph):
        return False, "Graph is partitioned"
    
    for node, node_resources in resources.items():
        if node not in graph.nodes:
            return False, f"Node {node} is not present in the graph"
        graph.nodes[node]['resources'] = node_resources
    
    return True, graph


# Exemplo de uso
def read_and_validate_network(input_file):
    try: 
        valid, graph = validate_graph(input_file)
        if valid:
            print(graph)
            print("O grafo é válido!")
            return graph
        else:
            print(graph)
            print("O grafo é inválido!")

        return None
    except:
        print("O grafo é inválido!")
        return None
