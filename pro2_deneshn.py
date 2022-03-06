#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import heapq

class Node:
    def __init__(self, x, y, cost, parent):
        
        self.x = x
        self.y = y
        self.cost = cost
        self.parent = parent

def Map(w,l):

    map = np.full((l,w),np.Infinity)
    radius=40
    
    for y in range(400):
        for x in range(250):
            # Defining a circle
            O = ((y -185)**2) + ((x-300)**2) - (radius)**2
            # Defining a Hexagon    
            h1 = y - 0.577*x - 24.97
            h2 = y + 0.577*x - 255.82
            h3 = x - 235
            h6 = x-165
            h5 = y + 0.577*x -175
            h4 = y - 0.577*x + 55.82
            # Defining an Irregular polygon   
            l1 = y- ((0.316)*x) - 173.608
            l2 = y + (1.23 *x) - 229.34
            l3 = y + (3.2*x) -436
            l4 = y - 0.857*x - 111.42
            l5 = y + (0.1136*x) - 189.09
            
            if(h1<0 and h2<0 and h3<0 and h4>0 and h5>0 and h6>0) or (O<0) or (l1<0 and l5>0 and l4>0)or (l2>0 and l5<0 and l3<0): 
                map[y,x]=2
                
            #Polygon's clearance
            pc1 = (y-5) - ((0.316) *(x+5)) - 173.608  
            pc2 = (y+5) + (1.23 * (x+5)) - 229.34 
            pc3 = (y-5) + (3.2 * (x-5)) - 436 
            pc4 = (y+5) - 0.857*(x-5) - 111.42 
            pc5 = y + (0.1136*x) - 189.09
            #Circle clearance
            Cc = ((y -185)**2) + ((x-300)**2) - (radius+5)**2
            #Hexagon clearance
            hc1 = (y-5) - 0.577*(x+5) - 24.97
            hc2 = (y-5) + 0.577*(x-5) - 255.82
            hc3 = (x-6.5) - 235 
            hc6 = (x+6.5) - 165 
            hc5 = (y+5) + 0.577*(x+5) - 175 
            hc4 = (y+5) - 0.577*(x-5) + 55.82 
        
            if(hc1<0 and hc2<0 and hc3<0 and hc4>0 and hc5>0 and hc6>0) or Cc<0  or (pc1<0 and pc5>0 and pc4>0)or (pc2>0 and pc5<0 and pc3<0):
                map[y,x]=1
                
    print(map)                    
    plt.imshow(map)
    ax = plt.gca()
    ax.invert_yaxis()
    plt.show()
        
    return map 

def Right(x, y, cost):
    x = x+1
    cost = cost + 1
    return x, y, cost

def Left(x, y, cost):
    x = x-1
    cost = cost + 1
    return x, y, cost

def Up(x, y, cost):
    y = y + 1
    cost = cost + 1
    return x, y, cost

def Down(x, y, cost):
    y = y - 1
    cost = cost + 1
    return x, y, cost

def Up_Right(x, y, cost):
    x = x + 1
    y = y + 1
    cost = cost + 1.4 
    return x, y, cost

def Up_Left(x, y, cost):
    x = x - 1
    y = y + 1
    cost = cost + 1.4
    return x, y, cost

def Down_Left(x, y, cost):
    x = x - 1
    y = y - 1
    cost = cost + 1.4
    return x, y, cost

def Down_Right(x, y, cost):
    x = x + 1
    y = y - 1
    cost = cost + 1.4
    return x, y, cost

def new_node(move, x, y, cost):
    if move == "right":
        return Right(x, y, cost)
    elif move == "left":
        return Left(x, y, cost)
    elif move == "up":
        return Up(x, y, cost)
    elif move == "down":
        return Down(x, y, cost)
    elif move == "upright":
        return Up_Right(x, y, cost)
    elif move == "upleft":
        return Up_Left(x, y, cost)
    elif move == "downleft":
        return Down_Left(x, y, cost)
    elif move == "downright":
        return Down_Right(x, y, cost)
    else:
        return None
    
    
def if_valid(x, y, map):
    
    shape = map.shape
    
    if (x > shape[0] or x < 0 or y > shape[1] or y < 0):
        return False
    else:    
        try:
            if(map[y][x] ==1) or map[y][x] == 2:
                return False
        except:
            pass
    return True

def check_goal(present, final):
    
    if(present.x == final.x) and (present.y == final.y):
        return True
    else:
        return False
    
def djikstra(initial, goal, map):
    
    if check_goal(initial, goal):
        return None,1
    
    actions = ["left", "right", "up", "down", "upleft", "upright", "downleft", "downright"]
    closed_dict = open_dict  = {}
    open_dict[(initial.x + initial.y*600)] = initial
    open_list = []
    all_nodes_list = []
    
    heapq.heappush(open_list,[initial.cost, initial])
    
    while(len(open_list)!=0):
        present_node = (heapq.heappop(open_list))[1]
        all_nodes_list.append([present_node.x, present_node.y])
        present_id = (present_node.x + present_node.y*600)
        
        if check_goal(present_node, goal):
            goal.parent = present_node.parent
            goal.cost = present_node.cost
            print("Reached Goal Coordinates Successfully!!!")
            return all_nodes_list,1
        
        if present_id in closed_dict:
            continue
        else:
            closed_dict[present_id] = present_node
            
        del open_dict[present_id]
        
        for move in actions:
            x, y, cost = new_node(move, int(present_node.x), int(present_node.y), present_node.cost)
            next_node = Node(x, y, cost, present_node)
            next_id = (next_node.x + next_node.y*300)
            if not if_valid (next_node.x, next_node.y , map) or (next_id in closed_dict):
                continue
            if next_id in open_dict:
                if next_node.cost < open_dict[next_id].cost:
                    open_dict[next_id].cost = next_node.cost
                    open_dict[next_id].parent = next_node.parent
                else:
                    open_dict[next_id] = next_node
                heapq.heappush(open_list, [open_dict[next_id].cost, open_dict[next_id]])
    return all_nodes_list,0

def backtrack(goal):
    path_x = [], path_y = []
    path_x.append(goal.x)
    path_y.append(goal.y)
    
    parent_node = goal.parent
    while parent_node != 0:
        path_x.append(parent_node.x)
        path_y.append(parent_node.y)
        parent_node = parent_node.parent
        
    return path_x, path_y

def plot(x_plot, y_plot, initial, goal, x_line, y_line, all_nodes_list):
    
    plt.plot(x_plot, y_plot, ".r")  
    plt.plot(initial.x,initial.y, "Do")
   # plt.plot(goal.x, goal.y, "Dg")
    plt.imshow(map, "reds")
    ax = plt.gca()
    ax.invert_yaxis()
    
    x_line.reverse()
    y_line.reverse()
    
    for i in range(len(all_nodes_list)):
        plt.plot(all_nodes_list[i][0], all_nodes_list[i][1], "3k")
        
    plt.plot(x_line, y_line, "-r")
    plt.show()
    plt.pause(5)
    plt.close("all")
    
if __name__ == '__main__':
    
    w = 400
    l = 250
    map = Map(w,l)
    i_coordinates = input("Enter the inital coordinates: ")
    x_initial, y_initial = i_coordinates.split()
    x_initial = int(x_initial)
    y_initial = int(y_initial)
    if not if_valid(x_initial, y_initial, map):
        print("Please enter a valid inital node: ")
        exit(0)
        
    f_coordinates = input("PLease enter the goal coordinates: ")
    x_final , y_final = f_coordinates.split()
    x_final = int(x_final)
    y_final = int(y_final)
    if not if_valid(x_final, y_final, map):
        print("Please enter a valid goal node: ")
        exit(0)
    
    initial = Node(x_initial, y_initial, 0.0, -1)
    goal = Node(x_final, y_final, 0.0, -1)
    all_nodes_list, goal_reached = djikstra(initial, goal, map)
    
    if (goal_reached)==1:
        x_line, y_line = backtrack(goal)
    else:
        print("Goal coordinates not found!!")
        exit(0)
        
    plot(initial, goal, x_line, y_line, all_nodes_list)