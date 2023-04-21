from db.user_db import USER_DATABASE
from utils.utils import check_graph_is_tree, check_relation, get_number_of_descendents
import logging
import os 

if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOGGING_LEVEL", default=logging.INFO))

    db = USER_DATABASE()
    db.initialize_tables() # CREATES THE REQUIRED TABLES (EDGES, NODES) and CREATES THE ROOT NODE
    cur = db.get_cursor()
    # SAMPLE DATA 

    db.insert_node("A1", "ROOT", "FIRST CHILD OF ROOT")  #              ROOT
    db.insert_node("A2", "ROOT", "SECOND CHILD OF ROOT") #            /   |   \
    db.insert_node("A3", "ROOT", "THIRD CHILD OF ROOT")  #           A1   A2  A3
    db.insert_node("B1", "A1", "FIRST CHILD OF A1")      #          /         /  \
    db.insert_node("B2", "A3", "FIRST CHILD OF A3")      #         B1        B2  B3
    db.insert_node("B3", "A3", "THIRD CHILD OF A3")      #
    db.insert_node("C1", "B1", "FIRST CHILD OF B1")

    print(check_relation(cur, "B1", "ROOT"))
    print(check_relation(cur, "B1", "B3"))
    print(check_relation(cur, "A1", "ROOT"))

    print(get_number_of_descendents(cur, "ROOT"))