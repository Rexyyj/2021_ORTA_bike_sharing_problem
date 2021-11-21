
from math import inf, radians
from operator import ne, xor
import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.core.numeric import zeros_like
import random
class RSM():

    def __init__(self,A,b,c,base,useful_x) -> None:
        self.A =A
        self.b =b
        self.c =c
        self.base = base
        self.useful_x =useful_x

        self.opt_pi = None
        self.opt_x = []
        self.opt_w = 0


    def rsm(self,basis):
        self.opt_pi ,temp_x = self.rsm_solver(basis)
        self.opt_x = temp_x[0:self.useful_x]
        for i in range(len(self.opt_x)):
            self.opt_w+=self.opt_x[i]*self.c[i]

    def rsm_solver(self,basis):
        mask = list(set(self.base)-set(basis))
        B = np.zeros((len(self.base),len(self.base)))
        for pos in basis:
            B[pos][pos]=1
        AB = np.matmul(self.A,B)
        idx = np.argwhere(np.all(AB[..., :] == 0, axis=0))
        AB = np.delete(AB, idx, axis=1)
        if np.linalg.matrix_rank(AB)!= len(AB):
            basis[random.randint(0,len(basis)-1)] = mask[random.randint(0,len(mask)-1)]
            return self.rsm_solver(basis)
        

        ABinv = np.linalg.inv(AB)
        cB = np.delete(np.matmul(self.c,B),mask)


        xB = np.matmul(ABinv,self.b)
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


A = np.array([[6,10,1,0,0,0],[8,5,0,1,0,0],[1,0,0,0,1,0],[0,1,0,0,0,1]])
b = np.array([2400,1600,500,100])
c =np.array([-24,-28,0,0,0,0])
base = [0,1,2,3,4,5]
init_basis = [1,2,3,4]
useful_x = 2

# A= np.array([[4,8,-1,1,0],[7,-2,2,0,-1]])
# b=[5,4]
# c=[3,2,6,0,0]
# base=[0,1,2,3,4]
# init_basis=[1,3]

# A= np.array([   [6,10,1,0,0,0,0,0],
#                 [8,5,0,1,0,0,0,0],
#                 [1,0,0,0,1,0,0,0],
#                 [1,0,0,0,0,-1,0,0],
#                 [0,1,0,0,0,0,1,0],
#                 [0,1,0,0,0,0,0,-1]
#             ])

# b=[2400,1600,500,0,100,0]
# c=[-24,-28,0,0,0,0,0,0]
# base =[0,1,2,3,4,5,6,7]
# init_basis =[0,1,2,3]

rsm = RSM(A,b,c,base,useful_x)
rsm.rsm(init_basis)
print(rsm.opt_pi)
print(rsm.opt_x)
print(rsm.opt_w)

# B = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

# pi = np.matmul(c,np.linalg.inv(AB))
# print(pi)