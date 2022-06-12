
from constraint import AllDifferentConstraint, Problem

def total_coloring(graph):
    
    #making dict to work with {key = node : value = integer}
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
