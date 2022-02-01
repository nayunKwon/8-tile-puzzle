# 8-tile puzzle 
# Used A* Search

import heapq
import copy

def goal(num):
    coordinate = []
    if num == 1:
        coordinate = [0,0]
    elif num == 2:
        coordinate = [0,1]
    elif num == 3:
        coordinate = [0,2]
    elif num == 4:
        coordinate = [1,0]
    elif num == 5:
        coordinate = [1,1]
    elif num == 6:
        coordinate = [1,2]
    elif num == 7:
        coordinate = [2,0]
    elif num == 8:
        coordinate = [2,1]
    
    return coordinate 

def heuristic(state):
    heuristic = 0 
    row = 0 
    col = 0

    for i in state:
        goal_coordinate = goal(i)
        if(i == 0):
            col += 1
            if col == 3 and col != 0:
                row += 1
                col = 0
            continue

        manhattan = abs(row - goal_coordinate[0]) + abs(col - goal_coordinate[1])
        # sum all the heuristic up 
        heuristic += manhattan

        #same row, next col
        col = col + 1

        if col != 0 and col == 3:
            col = 0
            row = row + 1 

    return heuristic 

def swap(state, i, j):
    ls = state.copy()
    ls[i] = state[j]
    ls[j] = state[i]
    return ls

def generate_succ(state):
    for i in range(9):
        if state[i] == 0:
            index = i
            break
    succ = []
    # num of succ state 
    # empty grid at the corner - 2
    if i in [0, 2, 6, 8]:
        if i == 0:              
                succ.append(swap(state, 0, 1))
                succ.append(swap(state, 0, 3))
        if i == 2:
                succ.append(swap(state, 2, 1))
                succ.append(swap(state, 2, 5))
        if i == 6:
                succ.append(swap(state, 6, 3))
                succ.append(swap(state, 6, 7))
        if i == 8:
                succ.append(swap(state, 8, 7))
                succ.append(swap(state, 8, 5))

    # empty grid at middle of boundary - 3
    elif i in [1, 3, 5, 7]:
        if i == 1:
                succ.append(swap(state, i, 0))
                succ.append(swap(state, i, 2))
                succ.append(swap(state, i, 4))
        if i == 3:
                succ.append(swap(state, i, 0))
                succ.append(swap(state, i, 4))
                succ.append(swap(state, i, 6))
        if i == 5:
                succ.append(swap(state, i, 2))
                succ.append(swap(state, i, 4))
                succ.append(swap(state, i, 8))
        if i == 7:
                succ.append(swap(state, i, 6))
                succ.append(swap(state, i, 4))
                succ.append(swap(state, i, 8))

    # empty grid is at center of boundary - 4 
    else:
        succ.append(swap(state, 4, 1))
        succ.append(swap(state, 4, 3))
        succ.append(swap(state, 4, 5))
        succ.append(swap(state, 4, 7))

    return sorted(succ)

def print_succ(state):
        succ = generate_succ(state)
        for i in succ:
            # print(i)
            h = str(heuristic(i))
            # print(h)
            print(i,'h=' + h)
    
def a_search(state,goal):
    open_ls = []
    close_ls = []
    que = []
    index = -1
    parents = {}

    current_state = state
    open_ls.append(current_state)
    heapq.heappush(que, (heuristic(state), state, (0, heuristic(state), index)))

    while len(que) > 0:
        # f=g+h, state, (g, h, parent_index)
        fn, current_state, g_h_parent = heapq.heappop(que)

        open_ls.remove(current_state)
        #store 
        close_ls.append(current_state)

        #if current state is same as the goal state, then return the path 
        if current_state == goal:
            return path(parents, current_state)

        for succ in generate_succ(current_state):

            # update the g(n) and f(n) = g(n)+ h
            g = g_h_parent[0] + 1
            f = g + heuristic(succ)

            if succ not in close_ls:
                parents[str(succ)] = current_state
                open_ls.append(succ)
                heapq.heappush(que,(f, succ, (g, heuristic(succ), index + 1)))

def path(parents, current_state):
    path_ls = []
    path_ls.append(current_state)

    while str(current_state) in parents.keys():
        current_state = parents[str(current_state)]
        path_ls.append(current_state)

    return path_ls

#  Given a state of the puzzle, perform the A* search algorithm and
#  print the path from the current state to the goal state
def solve(state):
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    a = a_search(state, goal)
    moves = 0
    
    for i in range(len(a)-1, -1, -1):
        print(a[i], 'h='+ str(heuristic(a[i])), 'moves: ' + str(moves))
        moves += 1
    return 

# print_succ([8,7,6,5,4,3,2,1,0])
# print(heuristic([8,7,6,5,4,3,2,1,0]))
# print(place(1))
# solve([1,2,3,4,5,6,7,0,8])
# solve([4,3,8,5,1,6,7,2,0])

if __name__ == "__main__":
    print_succ([1,2,3,4,5,0,6,7,8])
    solve([4,3,8,5,1,6,7,2,0])
    print_succ([8,7,6,5,4,3,2,1,0])
    solve([1,2,3,4,5,6,7,0,8])
