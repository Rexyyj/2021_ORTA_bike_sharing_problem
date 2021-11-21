
from math import inf, radians
from operator import ne, xor
import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.core.numeric import zeros_like
import random
class RSM():

    def __init__(self,A,b,c) -> None:
        self.A =A
        self.b =b
        self.c =c
        self.base = []
        for i in range(len(A[0])):
            self.base.append(i)

        self.opt_pi = None
        self.opt_x = None



    def rsm(self):
        basis = []
        for i in range(len(self.A)):
            basis.append(i)
        self.opt_pi ,self.opt_x = self.rsm_solver(basis)


    def rsm_solver(self,basis):
        print(basis)
        mask = list(set(self.base)-set(basis))
        B = np.zeros((len(self.base),len(self.base)))
        for pos in basis:
            B[pos][pos]=1
        AB = np.matmul(self.A,B)
        idx = np.argwhere(np.all(AB[..., :] == 0, axis=0))
        AB = np.delete(AB, idx, axis=1)
        ## ToDo: Imporve the basis update method
        if np.linalg.matrix_rank(AB)!= len(AB):
            basis[random.randint(0,len(basis)-1)] = mask[random.randint(0,len(mask)-1)]
            basis.sort()
            return self.rsm_solver(basis)
        

        ABinv = np.linalg.inv(AB)
        cB = np.delete(np.matmul(self.c,B),mask)


        xB = np.matmul(ABinv,self.b)
        ## ToDo: improve the basis update method
        if min(xB)<0:
            for k in range(len(xB)):
                if xB[k]<0:
                    rand_pos = random.randint(0,len(mask)-1)
                    basis[k] = mask[rand_pos]
                    basis.sort()
                    return self.rsm_solver(basis)

                    
        else:
            pi =np.matmul(cB,ABinv)
            neg_cost_pos = self.reduce_cost_test(mask,pi)
            if neg_cost_pos!=-1:
                mini_pos = self.minimum_ratio_test(neg_cost_pos,ABinv,xB)
                basis[mini_pos]=neg_cost_pos
                basis.sort()
                return self.rsm_solver(basis)
            else:
                return pi,xB

        
        
    def reduce_cost_test(self,mask,pi) -> int : # return the posistion of first found negetive cost
        min_var = inf
        pos = -1
        
        for var in mask:
            temp = np.transpose(self.A[:,var])
            cost = self.c[var]-np.matmul(pi,temp)
            if cost < 0:
                if cost < min_var:
                    min_var=cost
                    pos = var
        return pos


    def minimum_ratio_test(self,pos,ABinv,xB)-> int: # return the posisiton of basis to replace
        alpha = np.matmul(ABinv,np.transpose(self.A[:,pos]))
        ratio =[]
        for i in range(len(alpha)):
            ratio.append(xB[i]/alpha[i])
        min_ratio = min(ratio)
        for i in range(len(ratio)):
            if ratio[i]==min_ratio:
                return i
        return -1


if __name__ == "__main__":
    A = np.array([[6,10,1,0,0,0],[8,5,0,1,0,0],[1,0,0,0,1,0],[0,1,0,0,0,1]])
    b = np.array([2400,1600,500,100])
    c =np.array([-24,-28,0,0,0,0])


    rsm = RSM(A,b,c)
    rsm.rsm()
    print(rsm.opt_pi)
    print(rsm.opt_x)
