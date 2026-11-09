import os
import time
ACTIONS_STR =["down", "up", "right", "left"]
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Board:
    #empty index is a tuple (row, col)
    def __init__(self, data, size, empty_space_index, dist):
        self.data = tuple(data)
        self.size = size
        self.empty_space_index = empty_space_index
        self.dist = dist

    def __str__(self):
        rows = []

        for i in range(self.size):
            row = []
            for j in range(self.size):
                tile = self.tile_at(i, j)
                row.append(f"{tile:2}")

            rows.append(" ".join(row))

        return (
            "\n".join(rows)
            + f"\nEmpty index: {self.empty_space_index}"
            + f"\nManhattan distance: {self.dist}"
        )

    def tile_at(self, row, col):
        return self.data[row * self.size + col]

    def is_solvable(self):
        inversions = 0
        for i in range(len(self.data)):
            for j in range(i + 1, len(self.data)):
                if self.data[i] != 0 and self.data[j] != 0 and self.data[i] > self.data[j]:
                    inversions += 1
        if self.size % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions + self.empty_space_index[0]) % 2 == 1
    
    def caclulate_manhattan_distance_new(self, goal_positions):
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                tile = self.tile_at(i, j)
                if tile != 0:

                    distance += abs(i - goal_positions[tile-1][0]) + abs(j - goal_positions[tile-1][1])
        self.dist = distance
        return distance

    def caclulate_manhattan_distance(self, goal_positions, moving_tile_row, moving_tile_col):
        moving_tile = self.tile_at(moving_tile_row, moving_tile_col)
        minus_dist = abs(moving_tile_row - goal_positions[moving_tile-1][0]) + abs(moving_tile_col - goal_positions[moving_tile-1][1])
        plus_dist = abs(self.empty_space_index[0] - goal_positions[moving_tile-1][0]) + abs(self.empty_space_index[1] - goal_positions[moving_tile-1][1])
        return self.dist - minus_dist + plus_dist

    #function for gaol rows and collums
    # gaol_zero_index:
        # 0 - empty space in fist posion
        # n - empty space in last position
        #n/2 - empty space in the middle position
    def get_goal_positions(self, goal_zero_index):
        goal_positions = []
        n = self.size * self.size
        for tile in range(1,n):
            index = tile - int(tile <= goal_zero_index)
            target_row = index // self.size
            target_col = index % self.size
            goal_positions.append((target_row, target_col))
        return goal_positions

    def get_children(self, goal_positions):

        for i,action in enumerate(ACTIONS):
            moving_tile_row = self.empty_space_index[0] + action[0]
            moving_tile_col = self.empty_space_index[1] + action[1]
            if 0 <= moving_tile_row < self.size and 0 <= moving_tile_col < self.size:
                new_data = list(self.data)
                moving_tile_index = moving_tile_row * self.size + moving_tile_col
                empty_tile_index = self.empty_space_index[0] * self.size + self.empty_space_index[1]
                new_data[empty_tile_index], new_data[moving_tile_index] = new_data[moving_tile_index], new_data[empty_tile_index]
                new_dist= self.caclulate_manhattan_distance(goal_positions,  moving_tile_row, moving_tile_col)
                yield Board(new_data, self.size, (moving_tile_row, moving_tile_col), new_dist), ACTIONS_STR[i]
        
# IDA* logic

def ida_star(start, goal, goal_positions):
    limit = start.dist # Initial f-limit is just the heuristic of initial board

    while True:
        # Perform Depth-First Search with the current limit
        result, next_limit = dfs_search([], start, start, 0, limit, goal, goal_positions)

        if result: return result # Goal found!
        if next_limit == float('inf'): return None # No path exists

        limit = next_limit # Increase budget to the smallest value that exceeded previous limit

def dfs_search(path, current, previous, g, limit, goal, goal_positions):
    
    f = g + current.dist  # f(n) = g(n) + h(n)

    if f > limit: return None, f # Over budget! Return the exceeding f-value
    if current.data == goal: return path, f

    min_exceed = float('inf')
    # Explore neighbors in order
    for child, action in current.get_children(goal_positions):
        if child.data == previous.data: continue  # Don't go back to the parent
        path.append(action)
        res, next_f = dfs_search(path, child, current, g + 1, limit, goal, goal_positions)
        if res: return res, next_f
        min_exceed = min(min_exceed, next_f)
        path.pop()  # Backtrack if this branch doesn't find the goal

    return None, min_exceed

def main():
    #Pizzle size
    n = int(input())
    #Position of the empty space - 0 , n/2, (-1 or n-1)
    empty_space_index = int(input())
     #Claculete goal state
    goal_board = []
    if empty_space_index == 0:
        goal_board = [0]
    for i in range(n):
        goal_board.append(i + 1)
    if empty_space_index == n or empty_space_index == -1:
        empty_space_index = n
        goal_board.append(0)
    if empty_space_index == n // 2:
        goal_board.insert(n // 2, 0)
    goal_board = tuple(goal_board)
    #Input pizzle board
    initial_board = []
    board_size = int((n+1)**(0.5))
    for i in range(board_size):
        initial_board+=(list(map(int, input().split(" "))))

    # print(f"Initial board: {initial_board}")
    # print(f"Goal board: {goal_board}")

    #Start timer
    t = time.time()

    #Solve problem
    initial_board_obj = Board(initial_board, board_size, (initial_board.index(0) // board_size, initial_board.index(0) % board_size), 0)
    goal_positions = initial_board_obj.get_goal_positions(empty_space_index)
    initial_board_obj.caclulate_manhattan_distance_new(goal_positions)
    print_val = -1
    if not initial_board_obj.is_solvable():
        print_val = -1
        
    elif initial_board_obj.dist == 0:
        print_val = 0
    else:
        path = ida_star(initial_board_obj, goal_board, goal_positions)
        print_val = len(path) if path is not None else -1

    #print time
    print(f"# TIMES_MS: alg={int(time.time() - t) * 1000}")

    #print solution
    print(print_val)
    time_only = os.getenv("FMI_TIME_ONLY") == "1"
    if not time_only:
        if  print_val > 0:
            for action in path:
                print(action)

    


if __name__ == "__main__":
    main()