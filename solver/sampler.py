import numpy as np

class Sampler:
    
    def __init__(self) -> None:
        pass

    
    def sample_demand(self, n_scnario,config):
        
        data = np.around(np.random.uniform(
            0,
            config["staCap"],
            size=(n_scnario, config["staNum"],config["staNum"]))
        )
        for i in range(n_scnario):
            for j in range(config["staNum"]):
                data[i][j,j]=0
        prob = 1/n_scnario
        probList = np.linspace(prob,prob,n_scnario,dtype=float)
        return probList,data

