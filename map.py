from Nodes import Obstacles,start,goal,grid_size,check_node_obstacle_list,Node
import numpy as np

maze_canvas=np.full((grid_size[0],grid_size[1],3),(255,255,255))
obstacle_points=[]

def create_obstacles():

    global obstacle_points

    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            if(130+x>=y) and (290-7*x<=y) and ((17/3)*x-90<=y):
                node=Node(x,y)
                obstacle_points.append(node)
            # Complex shaped Obstacle
            if (x>=90 and 5*x-360<=y and y<=155) or (x>=90 and(x+530>=4*y) and ((5/6)*x+(170/3)<=y) and x<=130):
                node=Node(x,y)
                obstacle_points.append(node)
            # Complex shaped Obstacle
            if x>=120 and x<=160 and y>=35 and y<=130:
                if (x-10)>=y:
                    if x-400<=-2*y:
                        if 3*x-360<=y:
                            if x-60<=y or (-7/3)*x+(1120/3)>=y:
                                if (-2/5)*x +93<=y:
                                    node=Node(x,y)
                                    obstacle_points.append(node)
            # Triangular Shaped Obstacle
            if (2*x-340>=y) and ((-5/2)*x+605>=y) and (x-350>=-4*y):
                node=Node(x,y)
                obstacle_points.append(node)
            # Trapezoidal Shaped Obstacle
            if (-3*x+960>=y) and ((2/11)*x+(1460/11)>=y) and ((7/2)*x-(565)>=y) and (x+580<=5*y):
                node=Node(x,y)
                obstacle_points.append(node)

def load_map(maze_canvas):

    global obstacle_points
    if len(obstacle_points)>0:
        for nodes in obstacle_points:
            maze_canvas[nodes.x][nodes.y]=[0,0,0]

    return maze_canvas

create_obstacles()
maze_canvas=load_map(maze_canvas)
