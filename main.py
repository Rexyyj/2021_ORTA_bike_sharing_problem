#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
from operator import mod
from solver.twoStageModel import TwoStageMode
from solver.sampler import Sampler
import numpy as np

config ={
    "staNum":22,
    "staCap":30,
    "bikeCost":2,
    "stockOutCost":4,
    "tWastCost":8,
    "transhipCost":1,
}

sampler = Sampler()

prob,data_source = sampler.sample_demand(100,config)

model = TwoStageMode(100,config,data_source,prob)
model.solve()