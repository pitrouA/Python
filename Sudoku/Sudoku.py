#   1 2 3 4 5 6 7 8 9
# 1 - - - - - - - - -
# 2 - - - - - - - - -
# 3 - - - - - - - - -
# 4 - - - - - - - - -
# 5 - - - - - - - - -
# 6 - - - - - - - - -
# 7 - - - - - - - - -
# 8 - - - - - - - - -
# 9 - - - - - - - - -

import constraint
import json
import os

class Sudoku:

    NB_SOL = 20

    def __init__(self):
        self.problem = constraint.Problem() #le probleme a resoudre
        self.addSudokuConstraints()
    
    def __str__ (self):
        return self.printResult(self.problem)

    def addSudokuConstraints(self):
        # We're letting VARIABLES 11 through 99 have an interval of [1..9]
        for i in range(1, 10):
            self.problem.addVariables(range(i * 10 + 1, i * 10 + 10), range(1, 10))

        # We're adding the constraint that all values in a row must be different
        # 11 through 19 must be different, 21 through 29 must be all different,...
        for i in range(1, 10):
            self.problem.addConstraint(constraint.AllDifferentConstraint(), range(i * 10 + 1, i * 10 + 10))

        # Also all values in a column must be different
        # 11,21,31...91 must be different, also 12,22,32...92 must be different,...
        for i in range(1, 10):
            self.problem.addConstraint(constraint.AllDifferentConstraint(), range(10 + i, 100 + i, 10))

        # The last rule in a sudoku 9x9 puzzle is that those nine 3x3 squares must have all different values,
        # we start off by noting that each square "starts" at row indices 1, 4, 7
        for i in [1,4,7]:
            # Then we note that it's the same for columns, the squares start at indices 1, 4, 7 as well
            # basically one square starts at 11, the other at 14, another at 41, etc
            for j in [1,4,7]:
                square = [10*i+j,10*i+j+1,10*i+j+2,10*(i+1)+j,10*(i+1)+j+1,10*(i+1)+j+2,10*(i+2)+j,10*(i+2)+j+1,10*(i+2)+j+2]
                # As an example, for i = 1 and j = 1 (bottom left square), the cells 11,12,13,
                # 21,22,23, 31,32,33 have to be all different
                self.problem.addConstraint(constraint.AllDifferentConstraint(), square)

    def printResult(self, solutions):
        for s in solutions:
            print("==================")
            
            for i in range(1,10):
                print("|", end='')
                for j in range(1,10):
                    if j%3 == 0:
                        print(str(s[i*10+j])+" | ", end='')
                    else:
                        print(str(s[i*10+j]), end='')
                print("")
                if i%3 == 0 and i!=9:
                    print("------------------")
            print("==================")

        if len(solutions) == 0:
            print("No solutions found.")

    def castSolutionsToBoard(self, solutions):
        for s in solutions:
            print("==================")
            for i in range(1,10):
                print("|", end='')
                for j in range(1,10):
                    if j%3 == 0:
                        print(str(s[i*10+j])+" | ", end='')
                    else:
                        print(str(s[i*10+j]), end='')
                print("")
                if i%3 == 0 and i!=9:
                    print("------------------")
            print("==================")

        if len(solutions) == 0:
            print("No solutions found.")

    def getSolutions(self):
        solutions = []
        iter = self.problem.getSolutionIter()
        for _ in range(1,self.NB_SOL):
            solution = None
            try:
                solution = iter.__next__() #recupere la prochaine solution
            except Exception:
                break
            solutions.append(solution)#list(solution.values())
            #print(solution)
        return solutions
        # print(self.problem.getSolutions())
        # return self.problem.getSolutions()

    def clearEqualsConstraints(self):
        del self.problem
        self.problem = constraint.Problem()
        self.addSudokuConstraints()

    def addEqualsConstraintsToBoard(self, board):
        # We're adding a constraint for each number on the board (0 is an "empty" cell),
        # Since they're already solved, we don't need to solve them
        for i in range(1,10):
            for j in range(1,10):
                #print(board[i*10+j])
                if board[(i)*10 + (j)] != 0:
                    def equal_value_constraint(variable_value, value_in_table = board[(i)*10+(j)]):
                        if variable_value == value_in_table:
                            return True
                    # Basically we're making sure that our program doesn't change the values already on the board
                    # By telling it that the values NEED to equal the corresponding ones at the base board
                    self.problem.addConstraint(equal_value_constraint, [((i)*10+(j))])

