# Program that generates arborescences given a topology
# Author: Leon Okida
# Last changes: 03/28/2026

import networkx as nx
import copy

def _condition_1(r: str | int, c: int, graph: nx.DiGraph) -> bool:
    # Tests condition 1 to verify if it is possible to generate c arborescences
    aux = copy.deepcopy(graph)
    super_source = "condition_1_s"
    aux.add_node(super_source)

    for i in range(c):
        intermediate = f"condition_1_i_{i}"
        aux.add_edge(super_source, intermediate, capacity=1)
        aux.add_edge(intermediate, r, capacity=1)

    for vertex in sorted(graph.nodes()):
        if nx.algorithms.maximum_flow_value(aux, super_source, vertex, flow_func=nx.algorithms.flow.edmonds_karp) < c:
            return False
    
    return True

def _condition_2(r: str | int, u: str | int, v: str | int, c: int, j: int, graph: nx.DiGraph, used_arcs: set) -> bool:
    # Tests condition 2 to add an arc to the arborescence
    aux = copy.deepcopy(graph)
    for arc in used_arcs:
        aux.remove_edge(*arc)

    for i in range(j + 1, c):
        intermediate = f"condition_2_i_{i}"
        aux.add_edge(u, intermediate, capacity=1)
        aux.add_edge(intermediate, r, capacity=1)

    return nx.algorithms.maximum_flow_value(aux, u, v, flow_func=nx.algorithms.flow.edmonds_karp) >= c - j + 1

def _compute_r_rooted_arborescences(r: str | int, c: int, graph: nx.Graph) -> list[nx.DiGraph]:
    # Uses Tarjan's algorithm to generate c edje-disjoint r-rooted arborescences
    
    # Transforms graph into digraph
    digraph = graph.to_directed()

    used_arcs = set()
    arborescences = list()

    # Verifica condição 1 de existência de arborescências
    if not _condition_1(r, c, digraph):
        raise Exception(f"Failed condition 1 to generate {c} {r}-rooted arborescences")
    
    for j in range(1, c + 1):
        arbo = nx.DiGraph()
        arbo.add_node(r)
        # Generates initial candidate arcs set
        candidate_arcs = set(digraph.out_edges(r)) - used_arcs

        while len(arbo) < len(digraph):
            # Iteres over candidate arcs
            iterable_candidate_arcs = sorted(candidate_arcs)
            for u, v in iterable_candidate_arcs:
                # Removes arc e* from candidate arcs
                candidate_arcs.remove((u, v))
                
                # Continues if e* is not valid
                if v in arbo:
                    continue

                # Verifies condition 2
                # If true, increases the search space of candidate arcs
                if _condition_2(r, u, v, c, j, digraph, used_arcs):
                    arbo.add_edge(u, v)
                    used_arcs.add((u, v))
                    candidate_arcs.update(set(digraph.out_edges(v)) - used_arcs)
                    break

        if not nx.is_arborescence(arbo):
            raise Exception(f"Failed in creating #{j} {r}-rooted arborescence")

        # Reverses the arborescence to create routes to r
        arborescences.append(arbo.reverse())
        print(f"Created #{j} {r}-rooted arborescence")
    
    return arborescences

def generate_arborescences(graph: nx.Graph, root: str | int = None) -> dict[str | int, list[nx.DiGraph]]:
    # Computes the edge connectivity to find number of arborescences to generate
    c = nx.edge_connectivity(graph)
    print(f"The edge connectivity of the graph is: {c}")

    arborescences = dict()

    # If the root is not defined, the function generates arborescences for all destinations;
    # Else, it only generates arborescences for the desired root
    if root is not None:
        roots = [root]
    else:
        roots = graph.nodes

    # Iterates over roots
    for r in roots:
        # Generates c r-rooted arborescences
        r_arborescences = _compute_r_rooted_arborescences(
            r=r, 
            c=c,
            graph=graph
        )
        arborescences[r] = r_arborescences

    return arborescences
