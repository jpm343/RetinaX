#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 10:19:41 2017

@author: leo
"""
import glob
import pandas as pd

folder = '/home/cnsclab/filer/sim_noGABA/results/2017-06-05/'
filelist = glob.glob(folder + '*.txt')
folder = '/home/cnsclab/filer/sim_noGABA/results/2017-06-06/'
filelist = filelist + glob.glob(folder + '*.txt')

s = []
for f in filelist:
    r = f.split('_')[-1] 
    s.append(int(''.join(x for x in r if x.isdigit())))

rootstr = f.split('_array')[0] + '.txt'

filelist = [filelist[s.index(i)] for i in range(len(s))] # sorted

df = pd.DataFrame()
for f in filelist:
    df = df.append(pd.read_csv(f),ignore_index=True)
    
df.to_csv(rootstr)