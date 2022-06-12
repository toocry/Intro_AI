
from constraint import AllDifferentConstraint, Problem
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

def total_coloring(graph):
    """
        Find total chromatic index and total coloring.
        graph - instance of networkx.Graph
        returns - total chromatic index x
        Furthermore, assign property "color" for every vertex and edge. The value of the color has to be an integer between 0 and x-1.

        TASK: The implementation of this function finds some total coloring but the number of colors may not be minimal.
        Find the total chromatic index.
    """

    """"making dict to work with {key = node : value = integer}"""
    dict_nodes_num = {}
    node_num = 0
    max_deq = 0

    for node in graph.nodes():
        max_deq = max(max_deq, graph.degree(node))
        dict_nodes_num[node] = node_num
        node_num += 1
    
    num_of_colors = max_deq + 1

    dict_edges_num = {}
    edge_num = node_num

    for u,v in graph.edges():
        dict_edges_num[u,v] = edge_num
        dict_edges_num[v,u] = edge_num
        edge_num += 1
    
    
    while True:
        problem = Problem()
        problem.addVariables(dict_nodes_num.values(), range(num_of_colors))
   
        problem.addVariables(set(dict_edges_num.values()), range(num_of_colors))

       

     
        for node in dict_nodes_num:
          
            incident_list = [dict_nodes_num[node]]
            for u,v in graph.edges(node):
                incident_list.append(dict_edges_num[u,v])


            problem.addConstraint(AllDifferentConstraint(), incident_list)

            
            
            for neighbour in graph.neighbors(node):
                incident_list = [dict_nodes_num[node],dict_nodes_num[neighbour], dict_edges_num[node,neighbour]]
                problem.addConstraint(AllDifferentConstraint(), incident_list )

        solution = problem.getSolution()
        
        if solution != None:
        
            for u in graph.nodes():
                graph.nodes[u]["color"] = solution[dict_nodes_num[u]] 
            for u,v in graph.edges():
                graph.edges[u,v]["color"] = solution[dict_edges_num[u,v]]
            return num_of_colors

        num_of_colors += 1
