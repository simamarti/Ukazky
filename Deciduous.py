from Tree import Tree

class Deciduous():
    counter = 0
    
    def __init__(self):
        self.trees = []
    
    def addTree(self, tree : Tree) -> None:
        for t in self.trees:
            if t.name == tree.name:
                return None
            
        self.trees.append(tree)
        Deciduous.counter += 1