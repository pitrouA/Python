from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
import Board
import constraint
import json
import os
import Sudoku
import Board
import Solutions

class GUI(App):  
    switcher = {
        1: (0.6, 0.7, 0.2, 1),
        2: (0, 1, 1, 1),
        3: (1, 0, 1, 1),
        4: (1, 1, 0, 1),
        5: (0.5, 0.5, 1, 1),
        6: (0, 0.5, 0.5, 1),
        7: (0.5, 0, 0.5, 1),
        8: (0.3, 0.3, 0.3, 1),
        9: (0.7, 0.7, 0.7, 1),
        0: (1, 1, 1, 1)
    } 

    DIFFICULTY = 23

    selected_number = 1

    def on_button_press(self, obj:Button):
        print("Typical event from", obj)
        #obj.background_color = self.switcher.get(self.board.getValue(i,j))
        for i in range (1,10):
            for j in range (1,10):
                if self.buttonList[(i-1)*9+(j-1)] == obj: #objet trouve
                    print("objet trouve : "+str(i*10+j))
                    self.board.setValue(self.selected_number,i,j)
                    obj.text = str(self.selected_number)
            
        if(obj.text == ''):
            obj.background_color = (1, 1, 1, 1)
        else:
            obj.background_color = self.switcher.get(int(obj.text),(1, 1, 1, 1))

    def newGame(self):
        #-------------------------algo------------------------------
        jeu = Sudoku.Sudoku()
        jeu.addEqualsConstraintsToBoard(self.board.getBoard()) #ajoute les contraintes d'egalite sur les nombres deja presents
        print("solve start")
        solutions = Solutions.Solutions(jeu)
        print("solve end")
        #pas de solution
        while solutions.getSolutionNumber() > 1 :
            caseMax = solutions.getMaxCorrelationCase(self.board)
            self.board.setValue(solutions.getSolution(0).getValue(caseMax[0],caseMax[1]),caseMax[0], caseMax[1])
            print(self.board)
            jeu.clearEqualsConstraints()
            jeu.addEqualsConstraintsToBoard(self.board.getBoard())
            solutions = Solutions.Solutions(jeu)
        #-----------------------------------------------------------
        if(solutions.getSolutionNumber==0):
            print("No solution")
            return False
        print(self.board)
        self.updateButtonsColor()
        for i in range(1,10):
            for j in range(1,10):
                self.buttonList[(i-1)*9+(j-1)].text = '' #reset du texte de bouton
                if(self.board.getValue(i,j) != 0):
                    self.buttonList[(i-1)*9+(j-1)].text = str(self.board.getValue(i,j))
                    background_normal = self.buttonList[(i-1)*9+(j-1)].background_normal
                    #self.buttonList[(i-1)*9+(j-1)].disabled_color = self.buttonList[(i-1)*9+(j-1)].background_color
                    self.buttonList[(i-1)*9+(j-1)].disabled = True #desactive les nombres deja places
                    self.buttonList[(i-1)*9+(j-1)].background_disabled_normal = background_normal #remet la couleur de fond
                    self.buttonList[(i-1)*9+(j-1)].color = (1,1,1,1) #remet la couleur de texte
        print(self.board)
        return True

    def on_select_number(self, obj:Button):
        self.buttonListNumbers[self.selected_number-1].color = (1,1,1,1) #passe l'ancien bouton en blanc
        self.selected_number = int(obj.text)
        self.buttonListNumbers[self.selected_number-1].color = (1,0,0,1) #passe le nouveau bouton en rouge

    def on_load_game(self, obj:Button):
        print("load game")
        absolute_path = os.path.dirname(os.path.abspath(__file__)) #chemin absolu du fichier
        file_name = "sudoku" #nom du fichier du sudoku test
        
        self.board = Board.Board(absolute_path +"/"+file_name+"3.json")
        self.newGame()

    def on_new_game(self, obj:Button):
        print("new game")
        
        self.board = Board.Board()
        verite = self.board.setNumberAlea(self.DIFFICULTY)
        while not verite:
            verite = self.board.setNumberAlea(self.DIFFICULTY)
        verite = self.newGame()
        while not verite:
            verite = self.newGame()
        
        

    def updateButtonsColor(self):
        for i in range(1,10):
            for j in range(1,10):
                self.buttonList[(i-1)*9+(j-1)].background_color = self.switcher.get(self.board.getValue(i,j),(1, 1, 1, 1))


    def build(self):
        self.buttonList = []
        self.buttonListNumbers = []
        self.board = Board.Board()

        layout = RelativeLayout()
        layoutTop = GridLayout(cols=2,size_hint =(1, .2),pos_hint ={'x':0, 'top':1})
        layoutBottom = GridLayout(cols=2,size_hint =(1, .8), pos_hint ={'x':0, 'bottom':1})
        
        #---------- top ----------
        buttonLoad = Button(text="LoadGame")
        buttonLoad.bind(on_press=self.on_load_game)
        buttonNew = Button(text="NewGame")
        buttonNew.bind(on_press=self.on_new_game)
        layoutTop.add_widget(buttonNew)
        layoutTop.add_widget(buttonLoad)

        #---------- bottom ----------
        grid = GridLayout(cols=11,size_hint =(.9, 1)) #with separators
        
        i_ignore = 0
        for i in range(1,10):
            j_ignore = 0
            for j in range(1,10):
                btn = Button(text='', background_color=self.switcher.get(self.board.getValue(i_ignore,j-j_ignore),(1, 1, 1, 1)))
                btn.bind(on_press=self.on_button_press)
                self.buttonList.append(btn)
                grid.add_widget(btn)
                if j%3==0 and j<9:
                    grid.add_widget(Label())
                    j_ignore += 1
            if i%3==0 and i<9:
                for j in range(1,12): #with separators column
                    grid.add_widget(Label())
                i_ignore += 1

        gridNumbers = GridLayout(cols=1,size_hint =(.1, 1))
        for i in range(1,10):
            button = Button(text=""+str(i))
            button.background_color = self.switcher.get(i,(1, 1, 1, 1))
            if(i == self.selected_number):
                button.color = (1,0,0,1)
            button.bind(on_press=self.on_select_number)
            self.buttonListNumbers.append(button)
            gridNumbers.add_widget(button)

        layoutBottom.add_widget(grid)
        layoutBottom.add_widget(gridNumbers)

        #---------- principal ----------
        layout.add_widget(layoutTop)
        layout.add_widget(layoutBottom)

        return layout

    