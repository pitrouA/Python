

class Select():
    def __init__(self, pos:int, type:type):
        self.pos = pos
        self.type = type
        self.action = False

    def toogleMode(self):
        if self.action:
            self.action = False
        else:
            self.action = True
