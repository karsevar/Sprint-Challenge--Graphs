from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

## plan
# (COMPLETED)
# first create a depth first search function that can traverse the test_line.txt 
    # If the depth first search algorithm can traverse the straight line then 
    # the edge cases of having to turn back to unexplored nodes can be implemented

# (IN PROGRESS)
# second create a breadth first search function that can back track to rooms 
    # that haven't been fully explored. Namely the bfs while loop will terminate 
    # once it comes across a room with at least one '?'.

# stack data structure from the last project's utils
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# queue data structure from the last project's utils
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def found_question_mark(visited, room_id):
    '''
    Helper function for the breadth first search function.
    It loops through all the directions for a provided room id 
    in the visited dictionary and returns True if a question mark is 
    found and False if not
    '''
    for direction in visited[room_id]:
        # print('room id from found question mark', room_id)
        # print('room directions', direction, visited[room_id][direction])
        if visited[room_id][direction] == '?':
            return True 
    return False

def bfs(visited, current_room):
    '''
    This function will be a modification of the breadth first search from the 
    graphs.py file. This function accepts two arguments the traversal map (named in 
    the program as visited) and the id of the current room (which will be passed in 
    as current_room)
    '''
    # create a new visited variable which will be a set() in this function 
    # initialize a queue and place the current_room in the queue as [(current_room, 'NONE')]

    # create a while loop that will terminate once the queue is empty
        # dequeue the path from the queue the path will be visualized as an array 
        # containing tuples (room id, direction) example [(0, NONE), (1, n)]

        # if the last tuple in the path is not in visited:
            # check if room id in the last tuple has any question marks in any of the 
            # directions 
                # if so return the tuple path 
                # if not:
                    # loop through the directions using the room id from the last 
                    # tuple in the path visited[path[-1][0]]
                        # copy the path and append the neighboring rooms to the new_path
                        # example (visited[path[-1][0]][direction], direction) to get the following
                        # (room id, direction)
                        # append the newly created tuple to the new_path
                        # enqueue new_path array 
    visited_bfs = set()
    queue = Queue()
    queue.enqueue([(current_room, 'NONE')]) 

    while queue.size() > 0:
        path = queue.dequeue()

        # get the last tuple from the path
        current_direction = path[-1]

        if current_direction[0] not in visited_bfs:
            visited_bfs.add(current_direction[0])
            # will need to create a helper function to keep code clean
            # helper function found_question_mark 
            if found_question_mark(visited, current_direction[0]):
                return path 
            
            for direction in visited[current_direction[0]]:
                new_path = list(path)
                new_path.append((visited[current_direction[0]][direction], direction))
                queue.enqueue(new_path)

# used to reverse the directions for placement in the visited array 
reverse_direction = {
    'n':'s',
    's':'n',
    'w':'e',
    'e':'w'
}


def get_valid_exits(visited, current_room_id):
    '''
    returns an array of exits that have question marks as 
    values within the visited dictionary
    '''
    new_exits = []
    # print('visited array in get_valid exits', visited)

    for direction in visited[current_room_id]:
        if visited[current_room_id][direction] == '?':
            new_exits.append(direction)

    return new_exits


def dfs_modified(traversal_path, player):

    # create a visited array (this will be the traversal graph data structure in 
    # the readme)
        # example visited = {0: {n: ?, etc}}
    # initialize the visited array with the possible exits in room 0 
    # create a stack using the Stack class in the last project
        # this stack will hold the randomly chosen direction 
        # created from the command random.choice(player.current_room.get_exits())
    # initialize the stack with a randomly chosen direction from get_exits()
    # initialize a past_room variable that will hold the id of the past room 

    # while stack is not empty 
        # pop the direction off the stack 

        # check if the direction exists in the visited array as a key to a 
        # question mark 
            # if so:
                # move the player to the next room (player.travel(direction)) 
                # update the visited array with the new room key and possible 
                # directions 
                # place the direction in both the past_room's and current_room's 
                # key in the visited dictionary (in the current room's case the 
                # direction will need to be reversed)
                # get valid exits from a function that will return all exits that 
                # have a question mark value 
                # run random.choice() on the returned valid exits 

    visited = {}
    visited[player.current_room.id] = {}
    for direction in player.current_room.get_exits():
        visited[player.current_room.id][direction] = '?'
    
    past_room = player.current_room.id
    start_direction = random.choice(player.current_room.get_exits())
    stack = Stack()
    stack.push(start_direction)

    while stack.size() > 0:
        direction = stack.pop()

        if visited[player.current_room.id][direction] == '?':
            player.travel(direction) 
            # append direction to traversal_path
            traversal_path.append(direction)
            # update the visited dictionary with the current room's orientation to 
            # the past room 
            # example visited = {0: {n:1}}
            visited[past_room][direction] = player.current_room.id
            # update visited dictionary with the new room id and all possible room 
            # exits if the player.current_room.id is not in the visited dictionary 
            if player.current_room.id not in visited:
                visited[player.current_room.id] = {}
                for nsew in player.current_room.get_exits():
                    visited[player.current_room.id][nsew] = '?'
            # update the visited dictionary with the past room's orientation to the 
            # current room 
            visited[player.current_room.id][reverse_direction[direction]] = past_room
            # update past_room to read the id of the current_room
            past_room = player.current_room.id

            valid_exits = get_valid_exits(visited, player.current_room.id)
            # print('valid exits', valid_exits)
            # edge case if get_valid_exits function returns an empty array as 
            # the algorithm hit a deadend and will need to turn back

            # place breadth first search turn around logic here.
            # depth first search hit a deadend 
            if len(valid_exits) == 0:

                route = bfs(visited, player.current_room.id)
                # print('route back to unexplored', route)
                
                if route == None:
                    print('visited dictionary', visited)
                    return traversal_path 
                else:
                    for room in route[1:]:
                        player.travel(room[1])
                        traversal_path.append(room[1])

                    past_room = player.current_room.id
                    valid_exits = get_valid_exits(visited, player.current_room.id)

                    new_direction = random.choice(valid_exits)
                    stack.push(new_direction)


            else:

                new_direction = random.choice(valid_exits)
                stack.push(new_direction)       

                # print('visited dictionary', visited, 'past room', past_room)


dfs_modified(traversal_path, player)
print('traversal path', traversal_path)
    




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
