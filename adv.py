from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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
# first create a depth first search function that can traverse the test_line.txt 
    # If the depth first search algorithm can traverse the straight line then 
    # the edge cases of having to turn back to unexplored nodes can be implemented

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

# used to reverse the directions for placement in the visited array 
reverse_direction = {
    'n':'s',
    's':'n',
    'w':'e',
    'e':'w'
}

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
                for direction in player.current_room.get_exits():
                    visited[player.current_room.id][direction] = '?'
            # update the visited dictionary with the past room's orientation to the 
            # current room 
            visited[player.current_room.id][reverse_direction[direction]] = past_room
            # update past_room to read the id of the current_room
            past_room = player.current_room.id

    print('visited dictionary', visited, 'past room', past_room)

            
    

dfs_modified(traversal_path, player)
    




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
