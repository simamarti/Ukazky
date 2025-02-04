from Measurement import Measurement

class Iteration():
    def __init__(self, numIter : int):
        self.numIter = numIter
        self.clusterl1 = None
        self.clusterl2 = None
        self.voxel = None
        
    def addClusterl1(self, measurement):
        self.clusterl1 = measurement
        
    def addClusterl2(self, measurement):
        self.clusterl2 = measurement
        
    def addVoxel(self, measurement):
        self.voxel = measurement