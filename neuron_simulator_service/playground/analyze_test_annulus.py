#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:33:29 2017

@author: cnsclab
"""

import json
import numpy as np
import sys
import os


G_MIN_EXP = -6
G_MAX_EXP = -3
G_NUMBER = 20


gmax = np.logspace(G_MIN_EXP, G_MAX_EXP, G_NUMBER)

inner = (25, 50, 75, 100, 125, 150, 200)
outer = (75, 100, 125, 150, 175, 200, 250)

n_amac_rec = 1
n_var_rec = 2
amac_vecs = []
#synapse_vecs = []

#for PARAM_NUMBER in range(len(gmax)):
for PARAM_NUMBER in range(4,5):
    g = gmax[PARAM_NUMBER]
    simPath = "/home/cnsclab/filer/sim_annulus3/results%d/" % PARAM_NUMBER
    aux1 = []    
    for i, o in zip(inner, outer):        
        aux2 = []
        for k in range(n_amac_rec):
            aux3 = []
            for j in range(n_var_rec):
                aux3.append(np.loadtxt(simPath +
                           "amac_vecs_in%d_out%d_%d_%d.txt" % (i, o, k, j)))
            aux2.append(aux3)
        aux1.append(aux2)
    amac_vecs.append(aux1)
    
#        for k in range(n_amac_rec):
#            for j in range(n_var_rec):
#                synapse_vecs.append(np.loadtxt(simPath +
#                           "syn_vecs_in%d_out%d_%d_%d.txt" % (i, o, k, j)))

import matplotlib.pyplot as plt
#for PARAM_NUMBER in range(len(gmax)):
for PARAM_NUMBER in range(0,1):
    fig, ax = plt.subplots()
    pp = 0
    leg = []
    for i, o in zip(inner, outer):        
        plt.plot(4250*amac_vecs[PARAM_NUMBER][pp][0][0]) #area of 370um2, and times 10 to convert to pA
        leg.append(str(i))    
        pp += 1
    ax.set_ylim(0,5)
    plt.legend(leg)
