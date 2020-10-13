#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:42:48 2017

@author: cnsclab
"""

import matplotlib.pyplot as pl
from neuron import h
import numpy as np


h.load_file('stdrun.hoc')  # NEURON'S Libraries
h.CVode().active(1)
h.tstop = 2000

soma = h.Section()
syn_ = h.Exp2Syn(.5, sec=soma)

vclamp = h.SEClamp(.5, sec=soma)
vclamp.amp1 = -60
vclamp.dur1 = h.tstop


stim = h.NetStim()
stim.number = 5
stim.interval = 500.0
stim.start = 1.0
stim.noise = 0

recvec = h.Vector()

nc1 = h.NetCon(stim, syn_)
nc1.record(recvec)
nc1.weight[0] = 0.01
syn_.tau1 = 10
syn_.tau2 = 100

fs = 0.1

v = h.Vector(h.tstop/fs)
v.record(soma(.5)._ref_v,fs)
syn_i = h.Vector(h.tstop/fs)
syn_i.record(syn_._ref_i,fs)
syn_A = h.Vector(h.tstop/fs)
syn_A.record(syn_._ref_A,fs)
syn_B = h.Vector(h.tstop/fs)
syn_B.record(syn_._ref_B,fs)
syn_g = h.Vector(h.tstop/fs)
syn_g.record(syn_._ref_g,fs)

h.run()
fig, axs = pl.subplots(4,1)
t = np.arange(0,h.tstop,fs)
axs[0].plot(t, syn_i)
axs[1].plot(t, v) 
axs[2].plot(t, syn_B)
axs[3].plot(t, syn_g)
