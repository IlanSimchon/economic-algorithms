import math
import networkx as nx


def is_pareto_efficient(valuations, allocation):
    """
        Check if a given allocation is Pareto optimal.

        Args:
        - valuations (List[List[float]]): The valuation matrix where valuations[i][j] represents the value of item j for player i.
        - allocations (List[List[float]]): The allocation matrix where allocations[i][j] represents the amount of item j allocated to player i.

        Returns:
        - bool: True if the allocation is Pareto optimal, False otherwise.

        Examples:
        >>> valuations1 = [[10, 20, 30, 40], [40, 30, 20, 10]]
        >>> allocations1 =  [[0, 0.7, 1, 1], [1, 0.3, 0, 0]]
        >>> is_pareto_efficient(valuations1, allocations1)
        True

        >>> valuations2 = [[15, 25, 35, 45], [45, 35, 25, 15]]
        >>> allocations2 = [[0, 0.6, 1, 1], [1, 0.4, 0, 0]]
        >>> is_pareto_efficient(valuations2, allocations2)
        True

        >>> valuations2 = [[5, 2, 8], [8, 5, 2], [2, 8, 5]]
        >>> allocations2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        >>> is_pareto_efficient(valuations2, allocations2)
        False

        >>> valuations3 = [[12, 18, 24], [24, 12, 18], [18, 24, 12]]
        >>> allocations3 = [[0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5]]
        >>> is_pareto_efficient(valuations3, allocations3)
        False
    """

    def calculate_ratio(u, v, index):
        if valuations[v][index] == 0 or allocation[u][index] == 0:
            return math.inf
        return valuations[u][index] / valuations[v][index]

    num_nodes = len(valuations)
    graph = nx.DiGraph()

    for u in range(num_nodes):
        for v in range(num_nodes):
            if u != v:
                min_ratio = min(calculate_ratio(u, v, index) for index in range(len(valuations[u])))
                graph.add_edge(u, v, weight=math.log(min_ratio))

    for cycle in nx.simple_cycles(graph):
        cycle_weight_sum = round(sum(graph[u][v]['weight'] for u, v in zip(cycle, cycle[1:] + [cycle[0]])), 3)
        if cycle_weight_sum < 0:
            return False  # Found a cycle with sum of log-transformed weights greater than 1

    return True  # No such cycle found



if __name__ == '__main__':

    answer = is_pareto_efficient([[10, 20, 30, 40], [40, 30, 20, 10]],
                                 [[0, 0.7, 1, 1], [1, 0.3, 0, 0]])

    print(answer) # print True

    import doctest
    doctest.testmod()
