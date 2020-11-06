import GUI
from kivy.config import Config  


if __name__ == "__main__":
    Config.set('graphics', 'resizable', True)  
    gui = GUI.GUI()
    gui.run()
