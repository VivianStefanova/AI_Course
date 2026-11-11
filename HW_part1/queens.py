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
        self.conflicted_cols, self.conflicted_pos,self.conflicted_queens, self.conflict_values = self.queen_with_conflicts_init()
         #random generator 
        self.ties = []

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

    def queen_with_conflicts_init(self):
        n = self.n
        result_cols = []
        result_pos = {}
        conflict_values= [0]* n

        self.row_queens = [set() for _ in range(n)]
        self.diag1_queens = [set() for _ in range(2*n - 1)]
        self.diag2_queens = [set() for _ in range(2*n - 1)]
        
        count = 0
        row_queens = self.row_queens
        diag1_queens = self.diag1_queens
        diag2_queens = self.diag2_queens
        queens_per_row = self.queens_per_row
        queens_per_diag1 = self.queens_per_diag1
        queens_per_diag2 = self.queens_per_diag2
        for col, row in enumerate(self.board):
            row_queens[row].add(col)
            diag1_queens[row - col + n - 1].add(col)
            diag2_queens[row + col].add(col)
            conflicts = queens_per_row[row] - 1 # for the selected queen
            conflicts += queens_per_diag1[row - col + n - 1] - 1 
            conflicts += queens_per_diag2[row + col] - 1 
            conflict_values[col] = conflicts
            if conflicts > 0 : 
                result_pos[col] = count
                result_cols.append(col)
                count += 1
        return result_cols, result_pos, count,conflict_values


 
    # def update_qweens_conflicts(self, col, new_row):
    #     old_row = self.board[col]
    #     for c, row in enumerate(self.board):
    #         if c == col : continue
    #         old_conflicts = self.conflict_values[c]
    #         new_conflicts = self.conflict_values[c]
    #         if row == old_row : new_conflicts -= 1
    #         if row == new_row : new_conflicts += 1
    #         if row - c  == old_row - col : new_conflicts -= 1
    #         if row + c  == old_row + col : new_conflicts -= 1
    #         if row - c == new_row - col : new_conflicts += 1
    #         if row + c == new_row + col : new_conflicts += 1
    #         self.conflict_values[c] = new_conflicts
    #         if old_conflicts > 0 and new_conflicts == 0:
    #             self.remove_conflicted(c)
    #         if old_conflicts == 0 and new_conflicts > 0:
    #             self.add_conflicted(c)

    def update_qweens_conflicts(self, col, new_row):
        old_row = self.board[col]
        n = self.n

        old_d1 = old_row - col + n - 1
        old_d2 = old_row + col

        new_d1 = new_row - col + n - 1
        new_d2 = new_row + col

        affected = (
            self.row_queens[old_row] |
            self.row_queens[new_row] |
            self.diag1_queens[old_d1] |
            self.diag1_queens[new_d1] |
            self.diag2_queens[old_d2] |
            self.diag2_queens[new_d2]
        )
        board = self.board
        conflict_values = self.conflict_values
        for c in affected:
            if c == col:
                continue

            row = board[c]
            old_conflicts = conflict_values[c]
            new_conflicts = old_conflicts

            # Remove conflicts caused by the old position
            if row == old_row:
                new_conflicts -= 1

            if row - c == old_row - col:
                new_conflicts -= 1

            if row + c == old_row + col:
                new_conflicts -= 1

            # Add conflicts caused by the new position
            if row == new_row:
                new_conflicts += 1

            if row - c == new_row - col:
                new_conflicts += 1

            if row + c == new_row + col:
                new_conflicts += 1

            conflict_values[c] = new_conflicts

            if old_conflicts > 0 and new_conflicts == 0:
                self.remove_conflicted(c)

            elif old_conflicts == 0 and new_conflicts > 0:
                self.add_conflicted(c)
            


    def remove_conflicted(self, col):
        pos = self.conflicted_pos.pop(col)

        last = self.conflicted_cols.pop()
        self.conflicted_queens -= 1

        if pos < self.conflicted_queens:
            self.conflicted_cols[pos] = last
            self.conflicted_pos[last] = pos

    def add_conflicted(self, col):
        self.conflicted_pos[col] = self.conflicted_queens
        self.conflicted_cols.append(col)
        self.conflicted_queens +=1


    def update_board(self, col):
        old_row = self.board[col]
        new_row, min_row_conflict = self.get_min_conflict(col)

        if old_row == new_row:
            return

        n = self.n

        # Update conflicts of other queens
        self.update_qweens_conflicts(col, new_row)

        # Remove old position from indexes
        self.row_queens[old_row].remove(col)
        self.diag1_queens[old_row - col + n - 1].remove(col)
        self.diag2_queens[old_row + col].remove(col)

        # Update counters
        self.queens_per_row[old_row] -= 1
        self.queens_per_diag1[old_row - col + n - 1] -= 1
        self.queens_per_diag2[old_row + col] -= 1

        # Move queen
        self.board[col] = new_row

        # Add new position to indexes
        self.row_queens[new_row].add(col)
        self.diag1_queens[new_row - col + n - 1].add(col)
        self.diag2_queens[new_row + col].add(col)

        # Update counters
        self.queens_per_row[new_row] += 1
        self.queens_per_diag1[new_row - col + n - 1] += 1
        self.queens_per_diag2[new_row + col] += 1

        # Update selected queen
        old_conflicts = self.conflict_values[col]
        self.conflict_values[col] = int(min_row_conflict)

        if old_conflicts > 0 and min_row_conflict == 0:
            self.remove_conflicted(col)
            
        

 

    #Updates queen conflicts for the selected col
    # def get_min_conflict(self, col):
    #     min_conflicts = float('inf')
    #     min_rows = []
    #     for row in range(self.n):
    #         conflicts = self.queens_per_row[row]
    #         conflicts += self.queens_per_diag1[row - col + self.n - 1]
    #         conflicts += self.queens_per_diag2[row + col]

    #         # Exclude the current queen
    #         if row == self.board[col]:
    #             conflicts -= 3

    #         if conflicts < min_conflicts:
    #             min_conflicts = conflicts
    #             min_rows= [row]
    #         elif conflicts == min_conflicts:
    #             min_rows.append(row)
         
    #     return random.choice(min_rows), min_conflicts

    def get_min_conflict(self, col):
        n = self.n
        offset = n - 1 - col
        board_row = self.board[col]

        rows = self.queens_per_row
        diag1 = self.queens_per_diag1
        diag2 = self.queens_per_diag2
        ties = self.ties
        min_conflicts = n
        best_row = 0

        for row in range(n):
            conflicts = rows[row] + diag1[row + offset] + diag2[row + col]

            if row == board_row:
                conflicts -= 3

            if conflicts < min_conflicts:
                min_conflicts = conflicts
                ties = [row]
            elif conflicts == min_conflicts:
                ties.append(row)

        return random.choice(ties), min_conflicts

    

    def solve(self, max_iterations=100000):
        for _ in range(max_iterations):

            if self.conflicted_queens == 0:
                return self.board

            col = random.choice(self.conflicted_cols)

            self.update_board(col)

        return None

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
            pass
            #print(result)
            # print(board.queens_per_row)
            # print(board.queen_conflicts)
            # print(board)

    


if __name__ == "__main__":
    main()