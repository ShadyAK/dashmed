
CREATE_NODES_TABLE = '''
        CREATE TABLE nodes (
            name TEXT PRIMARY KEY,
            data TEXT,
            depth INTEGER
        )
    '''

CREATE_EDGES_TABLE = '''
        CREATE TABLE edges (
            id INTEGER PRIMARY KEY,
            parent_name TEXT,
            child_name TEXT,
            FOREIGN KEY(parent_name) REFERENCES nodes(name),
            FOREIGN KEY(child_name) REFERENCES nodes(name)
        )
    '''

MAKE_ROOT_NODE = "INSERT INTO NODES VALUES ('ROOT', 'ROOT NODE OF TREE', 0)"

