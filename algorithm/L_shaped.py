from math import inf

from numpy.core.getlimits import iinfo
from rsm import RSM
import numpy as np

class L_SHAPED():

    def __init__(self,init_master_A,init_master_b,init_master_c,base_master,init_sto_A,init_sto_b,init_sto_c,base_sto) -> None:
        self.r = 0
        self.s = 0
        self.v = 0

        self.master_A = init_master_A
        self.master_b = init_master_b
        self.master_c = init_master_c
        self.base_master = base_master

        self.sto_A = init_sto_A
        self.sto_b = init_sto_b
        self.sto_c = init_sto_c
        self.base_sto = base_sto


        self.theta = -inf
        self.x=[]


    def l_shaped(self):
        pass

    def solve_master(self):
        rsm = RSM(self.master_A,self.master_b,self.master_c)
        rsm.rsm()
        self.x = rsm.opt_x[0:self.base_master]


    def add_feasibility_cut(self):
        pass

    def check_optimal(self):
        pass

if __name__ == "__main__":

    init_master_A = np.array([[1,1,1,0,0],[1,0,0,-1,0],[0,1,0,0,-1]])
    init_master_b = np.array([120,40,20])
    init_master_c = np.array([100,150,0,0,0])
    base_master = 2

    init_sto_A = np.array([])
    init_sto_b = np.array([])
    init_sto_c = np.array([])
    base_sto = 2

    l_shaped = L_SHAPED(init_master_A,init_master_b,init_master_c,base_master,init_sto_A,init_sto_b,init_sto_c,base_sto)
    l_shaped.solve_master()
    print(l_shaped.x)