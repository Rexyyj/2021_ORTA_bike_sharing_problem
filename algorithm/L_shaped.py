from math import inf
from rsm import RSM
import numpy as np

class L_SHAPED():

    def __init__(self,init_master_A,init_master_b,init_master_c,base_master,init_sto_A,init_sto_b,init_sto_c,base_sto,samples) -> None:
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

        self.samples = samples


        self.theta = -inf
        self.x=[]


    def l_shaped(self):
        pass

    def solve_master(self):
        rsm = RSM(self.master_A,self.master_b,self.master_c)
        rsm.rsm()
        for i in range(len(rsm.opt_x)):
            if self.master_c[i]!=0:
                self.x.append(rsm.opt_x[i])
        #self.x = rsm.opt_x[0:self.base_master]

    def solve_stocastic(self):
        for sample in self.samples:
            A,b,c = self.get_sto_mat(self.x,sample)
            rsm = RSM(A,b,c)
            rsm.rsm()
            print(rsm.obj_min)
            del rsm
            pass

    def get_sto_mat(self,x,sample):
        # check the condition that A need to convert or not
        b = []
        c = []
        # merger sample and x
        dic = sample.copy()
        counter = 1
        for elem in x:
            key = "x"+str(counter)
            dic[key]=elem
            counter+=1

        for elem in self.sto_b:
            if isinstance(elem,str):
                b.append(self.mul_formular2val(elem,dic))
            elif isinstance(elem,int):
                b.append(elem)
            else:
                raise TypeError

        for elem in self.sto_c:
            if isinstance(elem,str):
                c.append(self.mul_formular2val(elem,dic))
            elif isinstance(elem,int):
                c.append(elem)
            else:
                raise TypeError
        return np.array(self.sto_A),np.array(b),np.array(c)

    def mul_formular2val(self,formular,dic):
        elem_val = 1
        for temp in formular.split("*"):
            multiplier = None
            try:
                multiplier = int(temp)
            except:
                multiplier = dic[temp]

            if multiplier!=None:
                elem_val*= multiplier
            else:
                raise ValueError
        return elem_val




    def add_feasibility_cut(self):
        pass

    def add_optimal_cut(self):
        pass

    def check_optimal(self):
        pass

if __name__ == "__main__":

    init_master_A = np.array([[1,1,1,0,0],[1,0,0,-1,0],[0,1,0,0,-1]])
    init_master_b = np.array([120,40,20])
    init_master_c = np.array([100,150,0,0,0])
    base_master = 2

    init_sto_A = [
        [6,10,1,0,0,0],
        [8,5,0,1,0,0],
        [1,0,0,0,1,0],
        [0,1,0,0,0,1]
    ]
    init_sto_b = ["60*x1","80*x2","d1","d2"]
    init_sto_c = ["q1","q2",0,0,0,0]
    base_sto = 2


    samples = [ {"d1":500,"d2":100,"q1":-24,"q2":-28,"p1":0.4},
                {"d1":300,"d2":300,"q1":-28,"q2":-32,"p1":0.6}]
    
    l_shaped = L_SHAPED(init_master_A,init_master_b,init_master_c,base_master,init_sto_A,init_sto_b,init_sto_c,base_sto,samples)
    l_shaped.solve_master()
    l_shaped.solve_stocastic()