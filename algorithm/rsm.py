
from math import inf
from operator import ne, xor
import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.core.numeric import zeros_like

def rsm(base,basis,A,b,c):
    mask = list(set(base)-set(basis))
    B = np.zeros((len(base),len(base)))
    for pos in basis:
        B[pos][pos]=1
    AB = np.matmul(A,B)
    idx = np.argwhere(np.all(AB[..., :] == 0, axis=0))
    AB = np.delete(AB, idx, axis=1)
    ABinv = np.linalg.inv(AB)
    cB = np.delete(np.matmul(c,B),mask)


    xB = np.matmul(ABinv,b)
    pi =np.matmul(cB,ABinv)
    
    pos=[]
    neg=[]

    for var in mask:
        cost = c[var]-np.matmul(pi,np.transpose(A[:,var]))
        if cost>=0:
            pos.append(var)
        else:
            neg.append(var)
    opt_pi=None
    if len(neg)!=0:
        alpha = np.matmul(ABinv,np.transpose(A[:,neg[0]]))
        rate=[]
        for i in range(len(alpha)):
            rate.append(xB[i]/alpha[i])
        min_pos=None
        min = inf
        for i in range(len(rate)):
            if rate[i]<min:
                min=rate[i]
                min_pos=i
        basis.remove(basis[min_pos])
        basis.append(neg[0])
        opt_pi = rsm(base,basis,A,b,c)
    else:
        opt_pi= pi

    return opt_pi



# A = np.array([[6,10,1,0,0,0],[8,5,0,1,0,0],[1,0,0,0,1,0],[0,1,0,0,0,1]])
# b = np.array([2400,1600,500,100])
# c =np.array([-24,-28,0,0,0,0])
# base = [0,1,2,3,4,5]
# basis = [2,3,4,5]

A= np.array([[4,8,-1,1,0],[7,-2,2,0,-1]])
b=[5,4]
c=[3,2,6,0,0]
base=[0,1,2,3,4]
basis=[0,1]

opt_pi = rsm(base,basis,A,b,c)
print(opt_pi)


# B = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

# pi = np.matmul(c,np.linalg.inv(AB))
# print(pi)