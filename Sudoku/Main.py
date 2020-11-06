import GUI
from kivy.config import Config  


if __name__ == "__main__":
    
    #print("####\n\n\n#####")

    #---sudoku2---
    #board2 = Board.Board(absolute_path +"/"+file_name+"2.json")
    #jeu.clearEqualsConstraints()
    #jeu.addEqualsConstraintsToBoard(board2.getBoard()) #ajoute les contraintes d'egalite sur les nombres deja presents
    #solutions2 = Solutions.Solutions(jeu)
    #print(solutions2)
    #print(solutions2.getCorrelationMatrix())
    #print(solutions2.getMaxCorrelationCase())
      
    Config.set('graphics', 'resizable', True)  
    gui = GUI.GUI()
    #gui.setBoard(board1)
    gui.run()
