
from pysat.solvers import Glucose3

def total_coloring(graph):

    """
           Find total chromatic index and total coloring.
           graph - instance of networkx.Graph
           returns - total chromatic index x
           Furthermore, assign property "color" for every vertex and edge. The value of the color has to be an integer between 0 and x-1.

           TODO: The implementation of this function finds some total coloring but the number of colors may be minimal.
           Find the total chromatic index.
       """

    max_deg = 0
    node_nums = {}
    node_num = 0
    for node in graph.nodes:
        max_deg = max(max_deg, graph.degree[node])
        node_nums[node] = node_num
        node_num += 1
    num_of_colors = max_deg + 1

    edge_nums = {}
    edge_num = node_num
    for u, v in graph.edges:
        edge_nums[u, v] = edge_num
        edge_nums[v, u] = edge_num
        edge_num += 1


    while True:
        g = Glucose3()
        count = 0
        variables = {}
        for v in node_nums.values():
            for c in range(num_of_colors):
                variables[(v, c)] = c + 1 + count * num_of_colors
            count += 1

        for e in set(edge_nums.values()):
            for c in range(num_of_colors):
                variables[(e, c)] = c + 1 + count * num_of_colors

            count += 1

        for v in graph.nodes():
            # constraint: at least 1 color for each node
            g.add_clause([variables[node_nums[v], c] for c in range(num_of_colors)])

            # constraint: each node is different color
            for i in range(num_of_colors):
                for j in range(i + 1, num_of_colors):
                    g.add_clause([-variables[node_nums[v], i], -variables[node_nums[v], j]])

            # constraint: neighbor edges of node V has the different color
            incident = [edge_nums[e] for e in graph.edges(v)]
            for c in range(num_of_colors):
                if len(incident) > 1:
                    for i in range(len(incident)):
                        for j in range(i + 1, len(incident)):
                            g.add_clause([-variables[incident[i], c], -variables[incident[j], c]])

        for u, v in graph.edges():
            # constraint: each edge has at least 1 color assigned
            g.add_clause([variables[edge_nums[u, v], c] for c in range(num_of_colors)])
            # constraint: edge should not have 2 or more colors assigned at a time
            for i in range(num_of_colors):
                for j in range(i + 1, num_of_colors):
                    g.add_clause([-variables[edge_nums[u, v], i], -variables[edge_nums[u, v], j]])

            for c in range(num_of_colors):
                #constraint: node U differs from node V
                g.add_clause([-variables[node_nums[u], c], -variables[node_nums[v], c]])
                # constraint: node U differs from edge U,V
                g.add_clause([-variables[node_nums[u], c], -variables[edge_nums[u, v], c]])
                #constraint: node V differs from U,V
                g.add_clause([-variables[node_nums[v], c], -variables[edge_nums[u, v], c]])

        if g.solve():
            solution = g.get_model()

            for v in graph.nodes():
                var_v = node_nums[v]
                for color in range(num_of_colors):
                    if variables[var_v, color] in solution:
                        graph.nodes[v]["color"] = color
                        break

            for u, v in graph.edges():
                var_uv = edge_nums[u, v]
                for color in range(num_of_colors):
                    if variables[var_uv, color] in solution:
                        graph.edges[u, v]["color"] = color
                        break

            return num_of_colors

        num_of_colors += 1

