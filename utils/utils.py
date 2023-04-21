from collections import defaultdict
from sqlite3 import Cursor
import logging

'''
CONTAIN UTILITY FUNCTIONS TO HANDLE RECURRING TASKS
'''
def table_exists(table_name: str, cur: Cursor) -> bool:

    table_check = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    result = cur.execute(table_check).fetchall()
    if len(result):
        return True 
    return False


def check_graph_is_tree(cur: Cursor, child_node: str = None, parent_node: str = None) -> bool:
    graph = defaultdict(set)
    if child_node and parent_node:
        graph[parent_node].add(child_node)

    edges = cur.execute("SELECT * FROM edges;").fetchall()
    

    for _, parent, child in edges:
        graph[parent].add(child)
    visited = set()

    def is_cyclic(node, parent): #Checks whether there is a cycle in the graph, if cycle exists then this can not be a tree
        visited.add(node)
        for child in graph[node]:
            if child not in visited:
                if is_cyclic(child, node):
                    return True
            elif child != parent:
                return True
        return False
    
    roots = set(graph.keys()) - set(child for children in graph.values() for child in children)
    if len(roots) > 1:
        logging.watn("Since there are now more than 1 root I.E disconnected graph, we can not approve this transaction")
        return False
    
    cyclic = is_cyclic("ROOT", None)
    if cyclic:
        logging.warn("Since graph is now cyclic, we can not approve this transaction")
    
    return not cyclic

def node_exists(cur: Cursor, node_name: str) -> bool:
    query = cur.execute(f"SELECT * FROM nodes WHERE name = '{node_name}'")
    return True if len(query.fetchall()) else False

def check_relation(cur: Cursor, first_node_name: str, second_node_name: str) -> str:
    if not (node_exists(cur, first_node_name) and node_exists(cur, second_node_name)):
        logging.warn("One or both nodes does not exist in the nodes table, check node names again")
    
    first_node_depth = cur.execute(f"SELECT depth FROM nodes WHERE name='{first_node_name}'").fetchone()[0]
    scnd_node_depth = cur.execute(f"SELECT depth FROM nodes WHERE name='{second_node_name}'").fetchone()[0]

    if first_node_depth == scnd_node_depth:
        return f"Siblings at depth level {first_node_depth}"
    
    if first_node_depth - scnd_node_depth == 1:
        res = cur.execute(f"SELECT * from edges WHERE parent_name = '{second_node_name}' and child_name = '{first_node_name}'").fetchall()
        if res:         # Relation between 3 and 1                                        _ Root _
            return f"{second_node_name} is the parent of {first_node_name}"  #           1         2
                                                                             #          / \
                                                                             #         3   4
    
    if scnd_node_depth - first_node_depth == 1:
        res = cur.execute(f"SELECT * from edges WHERE parent_name = '{first_node_name}' and child_name = '{second_node_name}'").fetchall()
        if res:
            return f"{first_node_name} is the parent of {second_node_name}"
    
    if first_node_depth > scnd_node_depth:
        return f"{second_node_name} is the ancestor of {first_node_name}"
    
    return f"{first_node_name} is the ancestor of {second_node_name}"

def get_number_of_descendents(cur: Cursor, parent_node: str) -> int:

    result = 0
    res = cur.execute(f"SELECT child_name FROM edges WHERE parent_name = '{parent_node}'").fetchall()
    
    descendents = [name[0] for name in res] 

    result += len(descendents)
    for desc in descendents:
        result += get_number_of_descendents(cur, desc)
    return result
