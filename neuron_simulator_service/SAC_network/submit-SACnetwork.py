# -*- coding: utf-8 -*-"""
"""
Created on Thu Dec 12 10:31:47 2013

@author: porio
"""
from __future__ import division
import SACnetwork
import numpy as np
import time
from mpi4py import MPI
# import neuron as h
# import matplotlib as pl
import json
import datetime
import os
import iodef as io

# Parameters
###############################################################################
G_MIN_EXP = -6
G_MAX_EXP = -3
G_NUMBER = 20
VELOC_MIN_EXP = -1
VELOC_MAX_EXP = 2
VELOC_NUMBER = 20
###############################################################################

if os.path.exists('./submit-SACnetwork.json'):
    io.load_params_json('./submit-SACnetwork.json', globals())

gmax = np.logspace(G_MIN_EXP, G_MAX_EXP, G_NUMBER)
stimuliSpeed = np.logspace(VELOC_MIN_EXP, VELOC_MAX_EXP, VELOC_NUMBER)
synapse_type = SACnetwork.synapse_type  # Note this param is in SACnetwork.py

t = time.time()
comm = MPI.COMM_WORLD
numproc = comm.size  # Number of processes
start_time = time.time()
i = 0
today = datetime.date.today()

print "Simulation using " + synapse_type
print "Starting simulation using ", numproc, " process"

simPath = "./results/%s/" % today

# Parallelizing simulations
if comm.rank == 0:  # Process number
    if not os.path.exists(simPath):  # only process 0 attempts to create folder
        os.makedirs(simPath)
    for g in gmax:  # ,50,100,300,500,1000:
        for sp in stimuliSpeed:
            comm.send((g, sp), dest=i % numproc)
            i += 1
    for i in range(numproc):
        comm.send(None, dest=i)

# Call functions to parallelize
# Steady-state function
sc1i, sc2i = SACnetwork.gabaInit(SACnetwork.excGmin)
params = comm.recv(source=0)

results = []
while (params is not None):
    g, sp = params
    print g, sp, 'proc', comm.rank
    res = SACnetwork.main(stimvel=sp, gabaI=(
        sc1i, sc2i), excmax=g, rank=comm.rank)
    results.append(np.r_[sp, g, res])
    print res, 'proc', comm.rank,
    "Time elapsed: ", time.time() - start_time, "s"
    comm.send(res, dest=0)
    params = comm.recv(source=0)

results2 = comm.gather(results, root=0)

comm.send(None, dest=0)

if comm.rank == 0:

    reslist = np.array([item1 for item2 in results2 for item1 in item2])

    print reslist
    print "Time elapsed: ", time.time() - start_time, "s"
    numv = len(SACnetwork.amac_rec)
    numsc = len(SACnetwork.syn_rec)
    head_entries = ['v%dp' % n for n in range(numv)] + \
        ['DSv%d' % n for n in range(numv)] + \
        ['sc%dp' % n for n in range(numsc)] +\
        ['DSsc%d' % n for n in range(numsc)] +\
        ['sc%dpa' % n for n in range(numsc)] +\
        ['DSsca%d' % n for n in range(numsc)]

    head = 'vel,gmax,ancho,vel,' + ','.join(head_entries)

    np.savetxt(simPath +
               synapse_type + '_%s_%s_%s_gmax_data%s_heat-grande_%s.txt' %
               (SACnetwork.amac_rec[0], SACnetwork.amac_rec[1],
                SACnetwork.amac_rec[2], SACnetwork.dataidx, SACnetwork.today),
               np.array(reslist), fmt='%6g', delimiter=',', header=head)

    # Parameters
    grid = {'Initial speed': stimuliSpeed[0],
            'Final Speed': stimuliSpeed[-1],
            'Speed points': len(stimuliSpeed),
            'Initial conductance': gmax[0],
            'Final conductance': gmax[-1],
            'Conductance points': len(gmax)}

    with open(simPath +
              synapse_type + '_simulation_parameters_%s.json' %
              SACnetwork.today, 'w') as fp:
        json.dump(grid, fp)
        json.dump(SACnetwork.dataFiles, fp)
        json.dump(SACnetwork.recording, fp)
        json.dump(SACnetwork.neuron_sim_opts, fp)
        json.dump(SACnetwork.amacrines, fp)
        json.dump(SACnetwork.bipolar, fp)
        json.dump(SACnetwork.gaba_sacs, fp)

elapsed = time.time() - t

print "Total Execution time: %s seconds" % elapsed

# Plots
# pl.clf()
#
# pl.subplot(211)
# for vec in Vvecs:
#    vvec=vec[0].as_numpy()[0:int(h.tstop/sampinvl)]
#    pl.plot(np.arange(0,h.tstop,sampinvl),vvec)
#    vvec=vec[1].as_numpy()[0:int(h.tstop/sampinvl)]
#    pl.plot(np.arange(0,h.tstop,sampinvl),vvec)
#
# pl.legend(np.hstack([('Vnull%g'%(i+1),
# 'Vpref%g'%(i+1)) for i in range(len(Vvecs))]))
#
# pl.subplot(212)
# for vec in scvecs:
#    svec=vec[0].as_numpy()[0:int(h.tstop/sampinvl)]
#    pl.plot(np.arange(0,h.tstop,sampinvl),svec)
#    svec=vec[1].as_numpy()[0:int(h.tstop/sampinvl)]
#    pl.plot(np.arange(0,h.tstop,sampinvl),svec)
#
# pl.legend(np.hstack([('scnull%g'%(i+1),
#        'scpref%g'%(i+1)) for i in range(len(scvecs))]))
# pl.savefig("%d.png"%())
