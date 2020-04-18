

class Node:
    def __init__(self,value,point):
        self.value=value
        self.point=point
        self.H=0
        self.G=0
        self.parent=None