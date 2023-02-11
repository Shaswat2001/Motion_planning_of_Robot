from Nodes import check_nodes,check_NodeIn_list
from data_structure import PriorityQueue
import math

def manhattan_heuristic(node1,node2):
    '''
    This Function calculates the Manhattan distance between two nodes

    Arguments:
    node1-- Instance of class Node
    node2-- Instance of class Node

    Returns:
    man_dist-- Manhattan distance between node1 and node2
    '''
    # Coordinates in Node1
    (x1,y1)=node1.get_coordinates()
    #Coordinates in Node2
    (x2,y2)=node2.get_coordinates()
    #The Manhattan distance
    man_dist=abs(x1-x2)+abs(y1-y2)

    return man_dist

class BidirectionalAstar:

    def __init__(self,start,goal,graph):

        self.start = start
        self.goal = goal
        self.graph = graph

        # Forward Planning
        self.OPEN_ford = PriorityQueue()
        self.CLOSED_ford = []
        self.backtrack_node_frd = {}

        # Backward Planning
        self.OPEN_bck = PriorityQueue()
        self.CLOSED_bck = []
        self.backtrack_node_bck = {}

    def plan(self):

        vertices=self.graph.get_vertices()
        #returns an instance of start Node from the graph
        start_vertex=self.graph.same_node_graph(self.start)
        goal_vertex = self.graph.same_node_graph(self.goal)

        past_cost_frd={nodes:math.inf for nodes in vertices}
        past_cost_frd[start_vertex]=0

        past_cost_bck={nodes:math.inf for nodes in vertices}
        past_cost_bck[goal_vertex]=0

        # Start Node with past cost is inserted into the queue
        self.OPEN_ford.insert_pq(0, start_vertex)
        self.OPEN_bck.insert_pq(0,goal_vertex)

        while self.OPEN_ford.len_pq()>0 and self.OPEN_bck.len_pq()>0:
        # Node with lowest past_cost is removed from the queue
            current_ct,current_vt=self.OPEN_ford.pop_pq()

            if check_NodeIn_list(current_vt,self.backtrack_node_bck.keys()):
                print("The goal node is found")
                return self.extract_path(current_vt),self.CLOSED_ford,self.CLOSED_bck
            
            # the Node is added to the CLOSED list
            self.CLOSED_ford.append(current_vt)

            # the neighbours of current_vt from cost_graph
            neighbour=self.graph.get_neighbours(current_vt)
            for nbr,cost in neighbour.items():
                # If the neighbour is not already visited
                if not check_NodeIn_list(nbr,self.CLOSED_ford):

                    # getting the same Node instance as used in cost_graph
                    vertex_same=self.graph.same_node_graph(current_vt)
                    nbr_same=self.graph.same_node_graph(nbr)

                    # the tentatative_distance is calculated
                    tentatative_distance=past_cost_frd[vertex_same]+cost
                    # If the past_cost is greater then the tentatative_distance
                    if past_cost_frd[nbr_same]>tentatative_distance:
                        # the neigbour node along with its parent and cost is added to the Dict
                        self.backtrack_node_frd[nbr_same]=vertex_same
                        past_cost_frd[nbr_same]=tentatative_distance
                        # Chosen heuristic is added to the tentatative_distance before adding it to the queue
                        tentatative_distance+=manhattan_heuristic(self.goal,nbr_same)
                        # Node along with the cost is added to the queue
                        self.OPEN_ford.insert_pq(tentatative_distance, nbr_same)
            
            current_ct,current_vt=self.OPEN_bck.pop_pq()

            if check_NodeIn_list(current_vt,self.backtrack_node_frd.keys()):
                print("The goal node is found")
                return self.extract_path(current_vt),self.CLOSED_ford,self.CLOSED_bck
            
            # the Node is added to the CLOSED list
            self.CLOSED_bck.append(current_vt)

            # the neighbours of current_vt from cost_graph
            neighbour=self.graph.get_neighbours(current_vt)
            for nbr,cost in neighbour.items():
                # If the neighbour is not already visited
                if not check_NodeIn_list(nbr,self.CLOSED_bck):

                    # getting the same Node instance as used in cost_graph
                    vertex_same=self.graph.same_node_graph(current_vt)
                    nbr_same=self.graph.same_node_graph(nbr)

                    # the tentatative_distance is calculated
                    tentatative_distance=past_cost_bck[vertex_same]+cost
                    # If the past_cost is greater then the tentatative_distance
                    if past_cost_bck[nbr_same]>tentatative_distance:
                        # the neigbour node along with its parent and cost is added to the Dict
                        self.backtrack_node_bck[nbr_same]=vertex_same
                        past_cost_bck[nbr_same]=tentatative_distance
                        # Chosen heuristic is added to the tentatative_distance before adding it to the queue
                        tentatative_distance+=manhattan_heuristic(self.start,nbr_same)
                        # Node along with the cost is added to the queue
                        self.OPEN_bck.insert_pq(tentatative_distance, nbr_same)
                            
        # If a path Doesn't exit
        print("The Goal coudnt be reached")
        return None,self.CLOSED_ford,self.CLOSED_bck
    

    def extract_path(self,meetNode):

        bkt_list=[]
        bkt_list.append(meetNode)
        node = meetNode
        # loops till goal is not equal to zero

        while node!=0:
            for nbr,parent in reversed(list(self.backtrack_node_bck.items())):
                # if nbr and goal are same
                if check_nodes(nbr,node):

                    if not check_NodeIn_list(parent,bkt_list):
                        bkt_list.append(parent)

                    node=parent

                    if check_nodes(parent,self.goal):
                        node=0
                        break
                    
        bkt_list.reverse()
        node = meetNode

        while node!=0:
            for nbr,parent in reversed(list(self.backtrack_node_frd.items())):
                # if nbr and goal are same
                if check_nodes(nbr,node):

                    if not check_NodeIn_list(parent,bkt_list):
                        bkt_list.append(parent)

                    node=parent

                    if check_nodes(parent,self.start):
                        node=0
                        return bkt_list