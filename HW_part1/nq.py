import time
import os
import random


def main():
    #Number of queens
    n = int(input())

    t = time.time()
    # index = collumn, value = row
    board = []
    
    #Solve problem
    #to_str(n_test, test)
    if n == 2 or n == 3 :
        board = None
    else: 
         
        board = list(range(1, n, 2)) + list(range(0, n, 2))
        queens_per_row = [1] * n
        diag1 = [0] * (2 * n- 1)  # \
        diag2 = [0] * (2 * n - 1)  # /
            
        for col, row in enumerate(board):
            diag1[row - col + n - 1] += 1
            diag2[row + col] += 1
        queens_per_diag1 = diag1
        queens_per_diag2 = diag2

        #random generator 
        ties = []
        if n % 6 == 2 or n %6 == 3:
            solved = False
            while not solved:
                solved = True
            
                n_1 = n-1
                max_conflict = float('-inf')
                max_col = 0 
                for col, row in enumerate(board):
                    conflicts = queens_per_row[row] + queens_per_diag1[row - col + n_1] + queens_per_diag2[row + col] - 3
                    if conflicts > 0 : solved = False
                    if conflicts > max_conflict:
                        max_conflict = conflicts
                        ties = [col]
                    elif conflicts == max_conflict:
                        ties.append(col)
                max_col = random.choice(ties)
                # Check if its solved
                if solved : continue
        
        
                min_conflict = float('inf')
                min_row = 0 
                old_row = board [max_col]
                for row in range(n):
                    conflicts = queens_per_row[row] + queens_per_diag1[row - max_col + n_1] + queens_per_diag2[row + max_col] 
        
                    if row == old_row : conflicts -= 3
        
                    if conflicts < min_conflict:
                        min_conflict = conflicts
                        ties = [row]
                    elif conflicts == min_conflict:
                        ties.append(row)
                 
            
                min_row = random.choice(ties)
                # Update counters
                queens_per_row[old_row] -= 1
                queens_per_diag1[old_row - max_col + n_1] -= 1
                queens_per_diag2[old_row + max_col] -= 1
        
                # Move queen
                board[max_col] = min_row
        
                # Update counters
                queens_per_row[min_row] += 1
                queens_per_diag1[min_row - max_col + n_1] += 1
                queens_per_diag2[min_row + max_col] += 1
        
            
        

    #print time
    print(f"# TIMES_MS: alg={int(time.time() - t) * 1000}")

    #print solution
    
    time_only = os.getenv("FMI_TIME_ONLY") == "1"
    if not time_only:
        if board is None:
            print(-1)
        else: 
            print(board)
            # print(board.queens_per_row)
            # print(board.queen_conflicts)
            # print(board)

    


if __name__ == "__main__":
    main()