
## Total coloring

[Total coloring](https://en.wikipedia.org/wiki/Total_coloring) of a graph is the coloring of vertices and edges such that:

    1. vertices connected by an edge have different colors,
    2. edges sharing a common vertex have different colors and
    3. edges and their end-vertices have different colors. The total chromatic number of a graph is the minimum number of colors required for total coloring of the graph.

Program finds the total chromatic number using the **constraint satisfaction programming solver** with the library [python-constraint](https://pypi.org/project/python-constraint/).
Solution code in `total_csp.py` file.

Program finds the total chromatic number using the **SAT(Satisfiability of boolean formulas) solver** with the library [python-sat](https://pypi.org/project/python-sat/). 
Solution code in `total_sat.py` file.

A graph is given using the library [networkx](https://pypi.org/project/networkx/).

