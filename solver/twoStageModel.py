import numpy as np
import gurobipy as gp
from gurobipy import GRB


class TwoStageMode:

    def __init__(self, n_scenario, config, data, prob) -> None:
        self.model = gp.Model("TwoStageModel")
        self.n_scenario = n_scenario
        self.config = config
        self.n = config["staNum"]
        self.data = data
        self.prob = prob

        self.x = None
        self.Bijs = []
        self.IiPs = []
        self.IijMs = []
        self.roijs = []
        self.OiPs = []
        self.OiMs = []
        self.taoijs = []
        self.TiPs = []
        self.TiMs = []

        self.init_vars()
        self.init_obj()
        self.add_constrains()

    def init_vars(self):

        self.x = self.model.addMVar(shape=self.n, vtype=GRB.INTEGER, name="x")

        for i in range(self.n_scenario):
            self.Bijs.append(self.model.addMVar(
                shape=(self.n, self.n), vtype=GRB.INTEGER, name="Bij"+str(i)))
            self.IiPs.append(self.model.addMVar(
                shape=self.n, vtype=GRB.INTEGER, name="IiP"+str(i)))
            self.IijMs.append(self.model.addMVar(
                shape=(self.n, self.n), vtype=GRB.INTEGER, name="IiM"+str(i)))
            self.roijs.append(self.model.addMVar(
                shape=(self.n, self.n), vtype=GRB.INTEGER, name="roij"+str(i)))
            self.OiPs.append(self.model.addMVar(
                shape=self.n, vtype=GRB.INTEGER, name="OiP"+str(i)))
            self.OiMs.append(self.model.addMVar(
                shape=self.n, vtype=GRB.INTEGER, name="OiM"+str(i)))
            self.taoijs.append(self.model.addMVar(
                shape=(self.n, self.n), vtype=GRB.INTEGER, name="taoij"+str(i)))
            self.TiPs.append(self.model.addMVar(
                shape=self.n, vtype=GRB.INTEGER, name="TiP"+str(i)))
            self.TiMs.append(self.model.addMVar(
                shape=self.n, vtype=GRB.INTEGER, name="TiM"+str(i)))

    def init_obj(self):
        obj = self.x.sum()*self.config["bikeCost"]

        for s in range(self.n_scenario):
            for i in range(self.n):
                term1 = self.IijMs[s][i, :].sum()*self.config["stockOutCost"]
                term2 = self.OiMs[s][i]*self.config["tWastCost"]
                term3 = self.taoijs[s][i, :].sum()*self.config["transhipCost"]
                obj += self.prob[s]*(term1+term2+term3)

        self.model.setObjective(obj, GRB.MINIMIZE)

    def add_constrains(self):
        for i in range(self.n):
            self.model.addConstr(
                self.x[i] <= self.config["staCap"], name="con1-"+str(i))

        for s in range(self.n_scenario):
            print("Adding constrains for scenarion: "+str(s))
            for i in range(self.n):
                self.model.addConstr(self.IiPs[s][i]-self.IijMs[s][i, :].sum(
                ) == self.x[i]-self.data[s][i, :].sum(), name="con3-"+str(i)+"-"+str(s))
                self.model.addConstr(self.OiPs[s][i]-self.OiMs[s][i] == self.config["staCap"]-self.x[i] +
                                     self.Bijs[s][i, :].sum()-self.Bijs[s][:, i].sum(), name="con4-"+str(i)+"-"+str(s))
                self.model.addConstr(self.roijs[s][i, :].sum(
                ) == self.OiMs[s][i], name="con5-"+str(i)+"-"+str(s))
                self.model.addConstr(self.roijs[s][:, i].sum(
                ) <= self.OiPs[s][i], name="con6-"+str(i)+"-"+str(s))
                self.model.addConstr(self.TiPs[s][i]-self.TiMs[s][i] == self.config["staCap"] -
                                     self.OiPs[s][i]+self.roijs[s][:, i].sum()-self.x[i], name="con7-"+str(i)+"-"+str(s))
                self.model.addConstr(self.taoijs[s][i,:].sum()==self.TiPs[s][i],name="con8-"+str(i)+"-"+str(s))
                self.model.addConstr(self.taoijs[s][:,i].sum()==self.TiMs[s][i],name="con8-"+str(i)+"-"+str(s))
                for j in range(self.n):
                    self.model.addConstr(self.Bijs[s][i, j] == self.data[s][i, j] -
                                         self.IijMs[s][i, j], name="con2-"+str(i)+"-"+str(j)+"-"+str(s))

    def solve(self):
        self.model.update()
        print("Start optimaization...")
        self.model.optimize()
        print(self.x.X)
        print('Obj: %g' % self.model.objVal)
        self.model.write("out.mst")
