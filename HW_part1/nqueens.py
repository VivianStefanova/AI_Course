import time
import os
import random

#Print symbols
QUEEN_SYMBOL = "*"
EMPTY_SPACE_SYMBOL = "_"
DELIMITER_SYMBOL = " "


test = [1, 3, 0, 2]
n_test = 4

class Board:
    def __init__(self, n):
        self.n = n
        self.board = self.knight_init_board()
        self.queens_per_row = self.rows_init_board()
        self.queens_per_diag1, self.queens_per_diag2 = self.diag_init_board() # \   /
        #random generator 
        self.randrange = random.randrange
       
        

    def __str__(self):
        output = ""
        for i in range(self.n):
            str = []
            for j in range(self.n):
                if self.board[j] == i :
                    str.append(QUEEN_SYMBOL)
                else: str.append(EMPTY_SPACE_SYMBOL)
            output +=  DELIMITER_SYMBOL.join(str) + "\n"
        return output

    def knight_init_board(self):
        return list(range(1, self.n, 2)) + list(range(0, self.n, 2))

    def rows_init_board (self):
        return [1] * self.n 

    def diag_init_board(self):
        diag1 = [0] * (2 * self.n - 1)  # \
        diag2 = [0] * (2 * self.n - 1)  # /

        n = self.n
        for col, row in enumerate(self.board):
            diag1[row - col + n - 1] += 1
            diag2[row + col] += 1

        return diag1, diag2

    
    def update_board(self):
        solved = True
        board = self.board
        queens_per_row = self.queens_per_row 
        queens_per_diag1 = self.queens_per_diag1
        queens_per_diag2 = self.queens_per_diag2
        n = self.n

        randrange = self.randrange

        max_conflict = float('-inf')
        tie_count = 0
        max_col = 0 
        for col, row in enumerate(board):
            conflicts = queens_per_row[row] + queens_per_diag1[row - col + n - 1] + queens_per_diag2[row + col] - 3
            if conflicts > 0 : solved = False
            if conflicts > max_conflict:
                max_conflict = conflicts
                max_col = col
                tie_count = 1
            elif conflicts == max_conflict:
                tie_count += 1
                if randrange(tie_count) == 0:
                    max_col = col

        # Check if its solved
        if solved : return solved


        min_conflict = float('inf')
        tie_count = 0
        min_row = 0 
        old_row = board [max_col]
        for row in range(n):
            conflicts = queens_per_row[row] + queens_per_diag1[row - max_col + n - 1] + queens_per_diag2[row + max_col] 

            if row == old_row : conflicts -= 3

            if conflicts < min_conflict:
                min_conflict = conflicts
                min_row = row
                tie_count = 1
            elif conflicts == min_conflict:
                tie_count += 1
                if randrange(tie_count) == 0:
                    min_row = row
         
    

        # Update counters
        queens_per_row[old_row] -= 1
        queens_per_diag1[old_row - max_col + n - 1] -= 1
        queens_per_diag2[old_row + max_col] -= 1

        # Move queen
        board[max_col] = min_row

        # Update counters
        queens_per_row[min_row] += 1
        queens_per_diag1[min_row - max_col + n - 1] += 1
        queens_per_diag2[min_row + max_col] += 1

        return solved

            
        

 

   

    

    def solve(self, max_iteration = 100000):
        update_board =self.update_board
        sovled = update_board()
        iteration = 0 
        while not sovled and iteration < max_iteration:
            sovled = update_board()
            iteration += 1

        return self.board

    # def solve(self, max_iterations=100000):
    #     for iteration in range(max_iterations):

    #         if self.conflicted_queens == 0:
    #             print("Solved:", iteration)
    #             return self.board

    #         col = self.get_max_conflict()
    #         new_row = self.get_min_conflict(col)

    #         self.update_board(col, new_row)

    #         if iteration % 1000 == 0:
    #             print(
    #                 iteration,
    #                 self.conflicted_queens,
    #                 sum(self.queen_conflicts)
    #             )

    #     print("Failed to converge")
    #     return None
        

    



def main():
    #Number of queens
    n = int(input())

    t = time.time()
    # index = collumn, value = row
    result = []
    

    


    #Solve problem
    #to_str(n_test, test)
    if n == 2 or n == 3 :
        result = None
    else: 
        board = Board(n)
        result = board.board
        if n % 6 == 2 or n %6 == 3:
            result = board.solve()
            
        

    #print time
    print(f"# TIMES_MS: alg={int(time.time() - t) * 1000}")

    #print solution
    
    time_only = os.getenv("FMI_TIME_ONLY") == "1"
    if not time_only:
        if result is None:
            print(-1)
        else: 
            
            print(result)
            # print(board.queens_per_row)
            # print(board.queen_conflicts)
            # print(board)

    


if __name__ == "__main__":
    main()