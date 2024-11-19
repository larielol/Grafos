import networkx as nx

def class_metrics(ddc, c):
    if(ddc == None or c == None):
        return None
    
    if not (c in ddc):
        return None
    
    if not(nx.is_directed(ddc)):
        return None
    
    return (ddc.out_degree(c),ddc.in_degree(c))
