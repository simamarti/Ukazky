from json import dump

from Deciduous import Deciduous
from Coniferous import Coniferous

class Database():
    def __init__(self):
        self.deciduous = Deciduous()
        self.coniferous = Coniferous()
    
    def addDeciduous(self, tree):
        self.deciduous.addTree(tree)
        
    def addConiferous(self, tree):
        self.coniferous.addTree(tree)
        
    def print(self):
        pass
    
    def save(self):
        saved = {}
        saved["Deciduous"] = {}
        saved["Deciduous"]["counter"] = self.deciduous.counter
        saved["Deciduous"]["trees"] = []
        
        for tree in self.deciduous.trees:
            treeJSON = {}
            treeJSON["name"] = tree.name
            treeJSON["type"] = tree.type
            treeJSON["original"] = {}
            
            treeJSON["original"]["numPoints"] = tree.original.numPoints
            treeJSON["original"]["perc"] = tree.original.perc
            treeJSON["original"]["percb2"] = tree.original.percb2
            treeJSON["original"]["iqr"] = tree.original.iqr
            treeJSON["original"]["mean"] = tree.original.mean
            treeJSON["original"]["skewness"] = tree.original.skewness
            treeJSON["original"]["percentiles"] = tree.original.percentiles
            
            treeJSON["iterations"] = []
            for iteration in tree.iterations:
                iterationJSON = {}
                iterationJSON["numIter"] = iteration.numIter
                iterationJSON["clusterl1"] = {}
                iterationJSON["clusterl2"] = {}
                iterationJSON["voxel"] = {}
                
                for measurement, maesurementJSON in \
                    zip([iteration.clusterl1,           iteration.clusterl2,        iteration.voxel], 
                        [iterationJSON["clusterl1"],    iterationJSON["clusterl2"], iterationJSON["voxel"]]):
                    
                    maesurementJSON["numPoints"] = measurement.numPoints
                    maesurementJSON["perc"] = measurement.perc
                    maesurementJSON["percb2"] = measurement.percb2
                    maesurementJSON["iqr"] = measurement.iqr
                    maesurementJSON["mean"] = measurement.mean
                    maesurementJSON["skewness"] = measurement.skewness
                    maesurementJSON["percentiles"] = measurement.percentiles
                
                treeJSON["iterations"].append(iterationJSON)
                
            treeJSON["numIteration"] = tree.numIteration
            
            saved["Deciduous"]["trees"].append(treeJSON)
            
        saved["Coniferous"] = {}
        saved["Coniferous"]["counter"] = self.coniferous.counter
        saved["Coniferous"]["trees"] = []
        
        for tree in self.coniferous.trees:
            treeJSON = {}
            treeJSON["name"] = tree.name
            treeJSON["type"] = tree.type
            treeJSON["original"] = {}
            
            treeJSON["original"]["numPoints"] = tree.original.numPoints
            treeJSON["original"]["perc"] = tree.original.perc
            treeJSON["original"]["percb2"] = tree.original.percb2
            treeJSON["original"]["iqr"] = tree.original.iqr
            treeJSON["original"]["mean"] = tree.original.mean
            treeJSON["original"]["skewness"] = tree.original.skewness
            treeJSON["original"]["percentiles"] = tree.original.percentiles
            
            treeJSON["iterations"] = []
            for iteration in tree.iterations:
                iterationJSON = {}
                iterationJSON["numIter"] = iteration.numIter
                iterationJSON["clusterl1"] = {}
                iterationJSON["clusterl2"] = {}
                iterationJSON["voxel"] = {}
                
                for measurement, maesurementJSON in \
                    zip([iteration.clusterl1,           iteration.clusterl2,        iteration.voxel], 
                        [iterationJSON["clusterl1"],    iterationJSON["clusterl2"], iterationJSON["voxel"]]):
                    
                    maesurementJSON["numPoints"] = measurement.numPoints
                    maesurementJSON["perc"] = measurement.perc
                    maesurementJSON["percb2"] = measurement.percb2
                    maesurementJSON["iqr"] = measurement.iqr
                    maesurementJSON["mean"] = measurement.mean
                    maesurementJSON["skewness"] = measurement.skewness
                    maesurementJSON["percentiles"] = measurement.percentiles
                
                treeJSON["iterations"].append(iterationJSON)
                
            treeJSON["numIteration"] = tree.numIteration
            
            saved["Coniferous"]["trees"].append(treeJSON)
            
        with open("database.geoJSON", 'w', encoding = 'utf-8') as f:
            dump(saved, f)