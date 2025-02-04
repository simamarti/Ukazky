class Measurement():
    def __init__(self,  numPoints : int,  perc : float, 
                        percb2 : float, iqr : float, 
                        mean : float, skewness : float, 
                        percentiles : list):
        
        self.numPoints = numPoints
        self.perc = perc
        self.percb2 = percb2
        self.iqr = iqr
        self.mean = mean
        self.skewness = skewness
        self.percentiles = percentiles