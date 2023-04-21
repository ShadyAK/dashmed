import os 
import sqlite3
from sqlite3 import Cursor, Connection
import constants.queries as QUERIES
import constants.constants as CONSTANTS
from utils.utils import check_graph_is_tree, node_exists
import logging

class USER_DATABASE:
    __dir_path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        try:
            os.remove(self.__dir_path+'/tree.db')
            logging.info("Old db removed for testing purpose, comment out line 16 in user_db.py to make the db persist its old data")
        except:
            pass 

        self.__conn = sqlite3.connect(self.__dir_path+'/tree.db')
        self.__cur = self.__conn.cursor()

    def __table_exists(self, table_name: str) -> bool: 

        table_check = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        result = self.__cur.execute(table_check).fetchall()
        
        return len(result) != 0
    
    def insert_node(self, node_name: str, parent_name: str, val: str): #Inserts node details in the nodes table
        try:
            if not node_exists(self.__cur, node_name) and node_exists(self.__cur, parent_name):
                depth = self.__cur.execute(f"SELECT depth FROM nodes WHERE name='{parent_name}'").fetchone()[0]
                insert_into_node_table = f"INSERT INTO nodes (NAME, DATA, DEPTH) VALUES ('{node_name}', '{val}', {depth+1})"
                self.__cur.execute(insert_into_node_table)
                self.insert_edge(node_name, parent_name)
                self.commit_change()
                logging.info(f"Inserted node {node_name} with val {val}")
            else:
                logging.warn(f"Node {node_name} already exists")

        except Exception as e:
            logging.error(f"Exception for {node_name} insertion: {e}")

    def insert_edge(self, node_name: str, parent_name: str): # Checks whether the node being added is valid or not and adds the node if it's valid
        try:
            cur = self.get_cursor()
            if check_graph_is_tree(cur, node_name, parent_name):
                insert_into_edge_table = f"INSERT INTO edges (parent_name, child_name) VALUES ('{parent_name}', '{node_name}') "
                self.__cur.execute(insert_into_edge_table)
                logging.info(f"Inserted edge {parent_name} -> {node_name}")
                self.commit_change()
            else:
                logging.warn("Can not insert the given relation")
        except Exception as e:
            logging.error(f"Exception: {e}")

    def commit_change(self):
        self.__conn.commit()
        logging.info("Changes commited successfully")
    
    def initialize_tables(self) -> None:
        if not self.__table_exists(CONSTANTS.NODES_TABLE_NAME):
            self.__cur.execute(QUERIES.CREATE_NODES_TABLE)
            self.__cur.execute(QUERIES.MAKE_ROOT_NODE) #We'll initialize out graph with a root node

        if not self.__table_exists(CONSTANTS.EDGES_TABLE_NAME):
            self.__cur.execute(QUERIES.CREATE_EDGES_TABLE)
        
        self.commit_change()

        if self.__table_exists("nodes") and self.__table_exists("edges"):
            logging.info("Tables successfully initialized")

    def print_tables(self) -> None:
        nodes = self.__cur.execute("SELECT * FROM nodes;").fetchall()
        
        print("_______NODES__________")
        for node in nodes:
            print(node)

        print("_________EDGES__________")
        edges = self.__cur.execute("SELECT * FROM edges;").fetchall()
        for edge in edges:
            print(edge)

    def close_connection(self) -> None:
        self.__conn.close()

    def get_cursor(self) -> Cursor:
        return self.__cur
    
    def get_conn(self) -> Connection:
        return self.__conn

    def rollback_last_transaction(self):
        self.__conn.rollback()