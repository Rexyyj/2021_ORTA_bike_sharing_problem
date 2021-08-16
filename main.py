#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
from operator import mod
from solver.twoStageModel import TwoStageMode
from solver.sampler import Sampler
import numpy as np

config ={
    "staNum":5,
    "staCap":30,
    "bikeCost":2,
    "stockOutCost":2,
    "tWastCost":4,
    "transhipCost":2,
}

sampler = Sampler()

prob,data_source = sampler.sample_normal(100,config)

model = TwoStageMode(100,config,data_source,prob)
model.solve()