# dashmed

## DB SCHEMA 

**NODES TABLE**   
   
   
NODE_NAME (__PRIMARY KEY__)      |    DATA    |    DEPTH    |   

Primary use of this table is store information about the node i.e DATA and storing DEPTH variable which is only set during initialization of that particular node and does not need any further transaction

Benifits - For extracting out the relation between two needs we do not need to traverse the whole tree and based on the relative depth of the nodes we can determine the positional relation between the nodes

**EDGES TABLE**

ID (Auto Increment)    |   CHILD_NAME (Foreign Key of NODES Table's primary key)   |    PARENT_NAME (Foreign Key of NODES Table's primary key) |


Use of this table is to have information about the relation between nodes and used in traversal during the checks when nodes are being added to prevent issues like loop in the graph and disconnected graphs



Some Tradeoff assumptions 

To count the number of descendents as mentioned in the assignment, I have assumed number of insertion operations will be much more than the number of times the functionality of calculating number of descendents of a node will be called. 
In the reverse case we could have stored another attribute named as descendents in our *NODES* table which would update on every addition of the node.
For example at depth 6 a node is added then all the pre-decessors of the node at 6th level would be traversed and the descendents attribute would be incremented by 1.
This would add O(H) time complexity in every addition of the node but will result in O(1) time complexity during calculation of number of descendents.



