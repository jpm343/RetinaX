#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 13:51:06 2017

@author: leo
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

#with open("results_paths.json",'r') as fp: 
#    p = json.load(fp)

def heat_map(plotPath, fn, thevar="DSsc"):

    filename = plotPath + fn
    data = np.loadtxt(filename, skiprows=1, delimiter=',')
    
    with open(filename) as f:
        lab = f.readline()
        lab = lab.replace(' ','') #old versions have spaces...
        labels = lab.split(',')
        data.shape = data.size
        data.dtype = [(l, float) for l in labels]
        data.sort(order=(labels[1], labels[3]))
    
    x = data['vel']
    y = data['gmax']
    
    sqsize = int(np.sqrt(len(data)))
    
    X = np.reshape(x,(-1,sqsize))
    Y = np.reshape(y,(-1,sqsize))
    
    SACS = fn.split('_')
    sacNames = []
    for i in range(len(SACS)):
        # if we found a number, it is a cell (TRUE), otherwise, FALSE
        sacNames.append(SACS[i].isdigit())
    
    sac_number = []
    for i in range(len(sacNames)):
        if(sacNames[i]):  # If true, I will save the sac number
            sac_number.append(SACS[i])
    
    plots = range(len(sac_number))  # how many plots? One for each SAC
    
    for sac in plots:
        z = data['sc%dp' % sac] * data['DSsc%d' % sac]
    #    z = data['DSsc%d' % sac]
        # z = data['sc%dp' % sac] * data['DSsc%d' % sac]
        z = data[thevar + str(sac)]
        # the following number must be concordant with the stimuli speed
        Z = np.reshape(z, (-1, sqsize))
        fig, ax = plt.subplots()
        # plt.clf()
        plt.title('SAC number: ' + str(sac_number[plots.index(sac)]))
        cax = ax.pcolor(X, Y, Z, vmin=0, vmax=.5)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_ylabel('$Stimulus\/\ intensity\/\ g_{max}$', fontsize=15)
        ax.set_ylim(min(y), max(y))
        ax.set_xlim(min(x), max(x))
        ax.set_xlabel('$Velocity\/\ (mm/s)$', fontsize=15)
        cbar = fig.colorbar(cax, ticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5])
        cbar.set_label('$DSI$', fontsize=15)
        plt.tight_layout()
        plt.savefig(plotPath + '/heatmap-' + thevar + str(sac) + '.png', dpi=300)
