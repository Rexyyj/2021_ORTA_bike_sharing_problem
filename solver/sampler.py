import numpy as np
import random
class Sampler:
    
    def __init__(self) -> None:
        pass

    
    def sample_uniform(self, n_scnario,config):
        data = []
        for i in range(n_scnario):
            data.append( np.around(np.random.uniform(
                random.randint(0,5),
                random.randint(5,10),
                size=(config["staNum"],config["staNum"]))
            ))
        for i in range(n_scnario):
            for j in range(config["staNum"]):
                data[i][j,j]=0
        prob = 1/n_scnario
        probList = np.linspace(prob,prob,n_scnario,dtype=float)
        return probList,data

    def sample_normal(self,n_scnario,config):
        data = []
        for i in range(n_scnario):
            data.append( np.around(np.abs(np.random.normal(
                10,
                10,
                size=(config["staNum"],config["staNum"])))
            ))
        prob = 1/n_scnario
        probList = np.linspace(prob,prob,n_scnario,dtype=float)
        return probList,data
    

