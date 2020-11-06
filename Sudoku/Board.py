import json
import array
from random import randrange

class Board:

    def __init__(self, path: str = None, solution: array = None):
        if(path != None):
            self.loadGame(path)
        elif(solution != None):
            self.board = solution
        else:
            self.fillBlank()

    def fillBlank(self):
        self.board = []
        for _ in range(0,10):
            for _ in range(0,10):
                self.board.append(0)

    def setNumberAlea(self, number:int):
        self.fillBlank()

        #for args numbers
        for _ in range(number):
            j = 0
            num = 0
            possible_j = []
            true_num = 10*[True]
            possible_num = []

            #alea i
            i = randrange(1,10)

            #alea j
            for j_loc in range(1,10):
                if self.getValue(i,j_loc)==0:
                    possible_j.append(j_loc)
            if len(possible_j)==1:
                j = possible_j[0]
            if len(possible_j)==0:
                return False
            j = possible_j[randrange(1,len(possible_j))]

            #lines
            for i_loc in range(1,10):
                if self.getValue(i_loc,j)!=0:
                    true_num[self.getValue(i_loc,j)]=False
            #column
            for j_loc in range(1,10):
                if self.getValue(i,j_loc)!=0:
                    true_num[self.getValue(i,j_loc)]=False
            #blocs
            i_bloc = int((i-1)-((i-1)%3))
            j_bloc = int((j-1)-((j-1)%3))
            for i_loc in range(1,4):
                for j_loc in range(1,4):
                    #print("i_bloc="+str(i_bloc)+" j_bloc="+str(j_bloc)+" i_loc="+str(i_loc)+" j_loc="+str(j_loc))
                    if self.getValue(i_bloc+i_loc,j_bloc+j_loc)!=0:
                        true_num[self.getValue(i_bloc+i_loc,j_bloc+j_loc)]=False
            #possible num
            for i_loc in range(1,10):
                if true_num[i_loc]:
                    possible_num.append(i_loc)
            if len(possible_num)==1:
                j = possible_num[0]
            if len(possible_num)==0:
                return False
            num = possible_num[randrange(1,len(possible_num))]

            print(str(num),str(i),str(j))

            #adding random num to grid with alea coordinates
            self.setValue(num,i,j)

        return True

    def loadGame(self, path):
        try:
            f = open(path, "r")
            jsonBoard = json.load(f)
            self.fillBlank()
            for i in range(1,10):
                for j in range(1,10):
                    #print(str(i)+" "+str(j))
                    self.board[i*10+j] = jsonBoard[i-1][j-1]
            f.close()
        except IOError:
            print ("Couldn't open file.")
            exit(0)

    #def addValueToGrid(self, value, x, y):
    #    self.board[x*10 + y] = value

    def getBoard(self):
        return self.board

    def setValue(self, value:int, i:int, j:int):
        self.board[i*10 + j] = value

    def getValue(self, i:int, j:int):
        return self.board[i*10 + j]

    def addBoards(self, board2:object):
        for i in range(1,10):
            for j in range(1,10):
                self.setValue(self.getValue(i,j)+board2.getValue(i,j),i,j)

    def removeBoard(self, board2:object):
        for i in range(1,10):
            for j in range(1,10):
                if board2.getValue(i,j)!=0 :
                    self.setValue(0, i, j)


    def getDifferences(self, board2:object):
        boardRet = Board()
        for i in range(1,10):
            for j in range(1,10):
                if board2.getValue(i,j) != self.getValue(i,j):
                    boardRet.setValue(boardRet.getValue(i,j)+1, i, j)
        return boardRet

    def __str__(self):
        ret = "==================\n"
        for i in range(1,10):
            ret = ret + "|"
            for j in range(1,10):
                if j%3 == 0:
                    ret = ret + str(self.getValue(i,j)) + " | "
                else:
                    ret = ret + str(self.getValue(i,j))
            ret = ret + "\n"
            if i%3 == 0 and i!=9:
                ret = ret + "------------------\n"
        ret = ret + "==================\n"
        return ret