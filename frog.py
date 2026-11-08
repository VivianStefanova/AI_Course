import time
import os

EMPTY_SPACE = "_"
#Direction of witch the frog is facing
LEFT_FROG = "<"
RIGHT_FROG = ">"

#Frog actions
ACTIONS= ["normal_leap_left", "double_leap_left", "normal_leap_right", "double_leap_right"]

class Tree:
    def __init__(self, n) -> None:
        self.n=n
        self.win = LEFT_FROG * n + EMPTY_SPACE + RIGHT_FROG * n
        self.start = RIGHT_FROG * n + EMPTY_SPACE + LEFT_FROG * n

    """Return the new configuration after the action"""
    def leap(self, action, config):
        if config == self.win:
            return config
        frogs_left,frogs_right=config.split("_")

        match action:
            case "normal_leap_left" if frogs_right and frogs_right[0] ==  LEFT_FROG: 
                return frogs_left + LEFT_FROG + EMPTY_SPACE + frogs_right[1:]
            case "double_leap_left" if len(frogs_right) > 1 and frogs_right[1] == LEFT_FROG:
                return frogs_left + LEFT_FROG + frogs_right[0] + EMPTY_SPACE + frogs_right[2:]
            case "normal_leap_right" if frogs_left and frogs_left[-1] ==  RIGHT_FROG: 
                return frogs_left[:-1] + EMPTY_SPACE + RIGHT_FROG + frogs_right
            case "double_leap_right" if len(frogs_left) > 1 and frogs_left[-2] == RIGHT_FROG:
                return frogs_left[:-2] + EMPTY_SPACE + frogs_left[-1] + RIGHT_FROG + frogs_right
        return None


    def get_children(self, parent):
        return (state for action in ACTIONS if (state := self.leap(action, parent)) is not None)

class DFS:
    
    def __init__(self, tree) -> None:
        self.tree=tree

    def dfs_helper(self, state, visited, path):
        if state == self.tree.win:
            return path + [state]
        
        if state in visited:
            return None
        visited.add(state)
        path.append(state)
        for child in self.tree.get_children(state):
            result = self.dfs_helper(child, visited, path)
            if result is not None:
                return result
            
        path.pop()  # Backtrack if this branch doesn't find the goal
        return None


    def dfs(self):
        state = self.tree.start
        visited = set()
        path = []
        return self.dfs_helper(state, visited, path)
        


def main():
    n = int(input())
    t = time.time()
    #Solve problem
    #test leap function
    tree = Tree(n)

    dfs = DFS(tree)
    path = dfs.dfs()

    #print time
    print(f"# TIMES_MS: alg={int(time.time() - t) * 1000}")

    #print solution
    time_only = os.getenv("FMI_TIME_ONLY") == "1"
    if not time_only:
        print("\n".join(path))

    


if __name__ == "__main__":
    main()