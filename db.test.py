import unittest
from db.user_db import USER_DATABASE
from utils.utils import check_graph_is_tree, check_relation, get_number_of_descendents
import logging
import os
'''
Only covering basic test cases covering most of the codebase for now and not including coverage metrics.
'''
class TestDBMethods(unittest.TestCase):

    logging.basicConfig(level=os.getenv("LOGGING_LEVEL", default=logging.INFO))

    def test_validate_graph_is_tree_when_given_right_inputs(self):
        db = USER_DATABASE()
        db.initialize_tables()
        cur = db.get_cursor()

        db.insert_node("1-1", "ROOT", "First node of first level")
        db.insert_node("1-2", "ROOT", "Second node of first level")
        db.insert_node("2-1", "1-1", "first element in depth level 2")
        db.insert_node("2-2", "1-1", "scond element in depth level 2")
        db.insert_node("2-3", "1-1", "Third element at depth 2")

        self.assertEqual(check_graph_is_tree(cur), True)
        
        
    def test_validate_insertion_error_when_loop_is_found_during_addition(self):
        db = USER_DATABASE()
        db.initialize_tables()
        cur = db.get_cursor()

        db.insert_node("1-1", "ROOT", "First node of first level")
        db.insert_node("1-2", "ROOT", "Second node of first level")
        db.insert_node("2-1", "1-1", "first element in depth level 2")
        db.insert_node("2-2", "1-1", "scond element in depth level 2")
        db.insert_node("2-3", "1-1", "Third element at depth 2")
        self.assertRaises(Exception, db.insert_edge("2-2", "2-1"))
         #This makes a loop in the graph which will throw an exception.

    def test_check_relation_functionality(self):
        db = USER_DATABASE()
        db.initialize_tables()
        cur = db.get_cursor()

        db.insert_node("1-1", "ROOT", "First node of first level")
        db.insert_node("1-2", "ROOT", "Second node of first level")
        db.insert_node("2-1", "1-1", "first element in depth level 2")
        db.insert_node("2-2", "1-1", "scond element in depth level 2")
        db.insert_node("2-3", "1-1", "Third element at depth 2")

        self.assertEqual(check_relation(cur, '1-1', '1-2'), "Siblings at depth level 1")
        self.assertEqual(check_relation(cur, '1-1', 'ROOT'), "ROOT is the parent of 1-1")
        
    def test_validate_number_of_descendents(self):
        db = USER_DATABASE()
        db.initialize_tables()
        cur = db.get_cursor()

        db.insert_node("1-1", "ROOT", "First node of first level")
        db.insert_node("1-2", "ROOT", "Second node of first level")
        db.insert_node("2-1", "1-1", "first element in depth level 2")
        db.insert_node("2-2", "1-1", "scond element in depth level 2")
        db.insert_node("2-3", "1-1", "Third element at depth 2")

        self.assertEqual(get_number_of_descendents(cur, "ROOT"), 5)
        
if __name__ == '__main__':
    unittest.main()