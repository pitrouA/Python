import Board

class Solutions:

    def __init__(self, jeu):
        self.solutions = []
        for solution in jeu.getSolutions():
            self.solutions.append(Board.Board(None,solution)) #trouve les solutions du probleme

    def __str__(self):
        ret = "###################\n#####Solutions#####\n###################\n"
        for solution in self.solutions:
            ret = ret + str(solution) + "###################\n"
        return ret

    def getSolutionNumber(self):
        return len(self.solutions)

    def getSolution(self, num:int):
        return self.solutions[num]

    def getCorrelationMatrix(self, board):
        correlationMatrix = Board.Board()
        baseSolution = self.solutions[0]
        baseSolution.removeBoard(board) #retirer les valeurs deja presentes sur le board pour ne pas avoir a les changer
        for solution in self.solutions[1:]:
            solution.removeBoard(board) #retirer les valeurs deja presentes sur le board pour ne pas avoir a les changer
            correlationMatrix.addBoards(baseSolution.getDifferences(solution))
        return correlationMatrix

    def getMaxCorrelationCase(self, board):
        correlationMatrix = self.getCorrelationMatrix(board)
        i_index = -1
        j_index = -1
        max_value = 0
        for i in range(1,10):
            for j in range(1,10):
                if correlationMatrix.getValue(i,j) > max_value:
                    i_index = i
                    j_index = j
                    max_value = correlationMatrix.getValue(i,j)
        return (i_index, j_index)
        