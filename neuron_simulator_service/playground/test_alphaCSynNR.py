#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:42:48 2017

This script compares alphaCSyn synapse with and w/o NET_RECEIVE
It also demonstrates the usefulness of NET_RECEIVE in that by using
NetCon/NetStim you can apply multiple stimuli, which was not possible
with the original version of alphaCSyn 

@author: cnsclab
"""

import matplotlib.pyplot as pl
from neuron import h
import numpy as np


h.load_file('stdrun.hoc')  # NEURON'S Libraries
h.CVode().active(1)
h.tstop = 2000

soma = h.Section()
syn_ = h.alphaCSynNR(.5, sec=soma)

stim = h.NetStim()
stim.number = 5
stim.interval = 500.0
stim.start = 1.0
stim.noise = 0

recvec = h.Vector()

nc1 = h.NetCon(stim, syn_)
nc1.record(recvec)
nc1.weight[0] = 0.01
syn_.tau = 10
syn_.dur = 100

fs = 0.1

v = h.Vector(h.tstop/fs)
v.record(soma(.5)._ref_v,fs)
syn_i = h.Vector(h.tstop/fs)
syn_i.record(syn_._ref_i,fs)
syn_A = h.Vector(h.tstop/fs)
syn_A.record(syn_._ref_a1,fs)
syn_B = h.Vector(h.tstop/fs)
syn_B.record(syn_._ref_a2,fs)
syn_g = h.Vector(h.tstop/fs)
syn_g.record(syn_._ref_g,fs)

h.run()
fig, axs = pl.subplots(4,1)
t = np.arange(0,h.tstop,fs)
axs[0].plot(t, syn_i)
axs[1].plot(t, v) 
axs[2].plot(t, syn_A)
axs[3].plot(t, syn_g)


#alphaCSyn
soma2 = h.Section()
syn2_ = h.alphaCSyn(.5, sec=soma2)

recvec = h.Vector()

syn2_.tau = 10
syn2_.dur = 100

fs = 0.1

v2 = h.Vector(h.tstop/fs)
v2.record(soma2(.5)._ref_v,fs)
syn2_i = h.Vector(h.tstop/fs)
syn2_i.record(syn2_._ref_i,fs)
syn2_A = h.Vector(h.tstop/fs)
syn2_A.record(syn2_._ref_a1,fs)
syn2_B = h.Vector(h.tstop/fs)
syn2_B.record(syn2_._ref_a2,fs)
syn2_g = h.Vector(h.tstop/fs)
syn2_g.record(syn2_._ref_g,fs)

h.run()
fig, axs = pl.subplots(4,1)
t = np.arange(0,h.tstop,fs)
axs[0].plot(t, syn2_i)
axs[1].plot(t, v2) 
axs[2].plot(t, syn2_A)
axs[3].plot(t, syn2_g)
