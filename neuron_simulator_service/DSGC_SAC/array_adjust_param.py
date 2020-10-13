"""
Created on May 2019

@author: Leo Medina
"""
from __future__ import division
from DSGC_SAC import *
import numpy as np
import time
import datetime
import os
import iodef as io
import sys

# Parameters
###############################################################################
G_MIN_EXP = -1
G_MAX_EXP = 1
G_NUMBER = 7
BP_MIN_EXP = -1
BP_MAX_EXP = 2
BP_NUMBER = 7
OLAP_MIN_EXP = 2
OLAP_MAX_EXP = 3
OLAP_NUMBER = 7
OLAP_FACTOR_MIN_EXP = 0
OLAP_FACTOR_MAX_EXP = 0
OLAP_FACTOR_NUMBER = 1
PARAM_NUMBER = sys.argv[1]
diag = np.sqrt(250 ** 2 + 300 ** 2)
angles = (0, 45, 90, 135, 180, 225, 270, 315)
d_inits = (0, 0, 0, diag, 2 * dsgc_x, 2 * diag, 2 * dsgc_y, diag)
sp = 1.61  # best SAC selectivity for this speed
SAC_excGmax = 4.25e-5  # best SAC selectivity for this stim level
###############################################################################


if os.path.exists('./array-DSGC-SAC.json'):
    io.load_params_json('./array-DSGC-SAC.json', globals())
if os.path.exists('./gabaInit.json'):
    print "Loading GABA initial parameters from file..."
    sc1i, sc2i = io.load_gabaInit_file('./gabaInit.json')
else:
    sc1i, sc2i = s.gabaInit(s.excGmin)

gabamax = np.logspace(G_MIN_EXP, G_MAX_EXP, G_NUMBER)
excmax = np.logspace(BP_MIN_EXP, BP_MAX_EXP, BP_NUMBER)
olap = np.logspace(OLAP_MIN_EXP, OLAP_MAX_EXP, OLAP_NUMBER)
olapfactor = np.logspace(OLAP_FACTOR_MIN_EXP,
                         OLAP_FACTOR_MAX_EXP, OLAP_FACTOR_NUMBER)
synapse_type = s.synapse_type  # Note this param is in SACnetwork.py
params = [(g, e, o, of)
          for g in gabamax for e in excmax for o in olap for of in olapfactor]

start_time = time.time()
today = datetime.date.today()

print "Simulation using " + synapse_type
print "Starting simulation: "

simPath = "./results/%s/" % today

if not os.path.exists(simPath):  # only process 0 attempts to create folder
    os.makedirs(simPath)

numv = len(s.amac_rec)
numsc = len(s.amac_rec)
head_entries = ['v%dp' % n for n in range(numv)] + \
    ['DSv%d' % n for n in range(numv)] + \
    ['sc%dp' % n for n in range(numsc)] +\
    ['DSsc%d' % n for n in range(numsc)] +\
    ['sc%dpa' % n for n in range(numsc)] +\
    ['DSsca%d' % n for n in range(numsc)]

head = 'exc,gaba,angle,nspk,width,speed,' + ','.join(head_entries)
head_dsi = 'exc,gaba,overlap,overlap_factor,dsi,dsi_angle180'

grid = {'Initial excitation': excmax[0],
        'Final excitation': excmax[-1],
        'excitation points': len(excmax),
        'Initial GABA': gabamax[0],
        'Final GABA': gabamax[-1],
        'GABA points': len(gabamax)}

if not isinstance(PARAM_NUMBER, list):
    PARAM_NUMBER = [PARAM_NUMBER]


res = []
res_dsi = []
for param_num in PARAM_NUMBER:
    gaba, exc, o, of = params[int(param_num)]
    print "Running sim with excitation %f gaba %f olap %f and olapfactor %f" % (exc, gaba, o, of)
    # Assuming a field of about 1 mm, simulation must be long enough for bar to
    # cover the entire field. sp in mm/s, multiply by 1000 to convert to ms
    t_total = s.t_es + (1.0 +
                        s.stim_param['bar_width'] /
                        1000.0) / sp * 1000.0
    if t_total < 1500:
        t_total = 1500  # Sim no shorter than 1.5 s, see calculation of DSI
    s.tstop = t_total
    gBPsyn = bipolar_DSGC_synapses(s)
    GABAsynpos, synM = SAC_DSGC_synapses(s, thresh=o, overlap_factor=of)

    nspk = []
    for (ang, d_init) in zip(angles, d_inits):
        stim_param['bar_speed'] = sp
        stim_param['bar_x_init'] = d_init
        stim_param['bar_angle'] = ang
        # Setting DSGC inputs ################################################
        # This is for DSGC inputs. Note that SAC syanpses are set and defined
        # SAC_network
        dscell.setv(-75.5, -75.5, -79)
        gBPsyn = s.topo.excGset(gBPsyn, gmax=exc * SAC_excGmax, gmin=excGmin,
                                synapse_type=synapse_type, tau=tau)
        s.stim.set_stimulus(gBPsyn, stimulus_type, t_inf, synapse_type,
                            **stim_param)
        s.topo.gabaGset(gSACsyn, synM, gaba * s.gabaGmax, gabaGmin,
                        k1, k2, th1, th2, e_rev)

        apcount = s.h.APCount(dscell.axon(.9))

        res_i, amac_vecs, synapse_vecs = s.main(excmax=SAC_excGmax,
                                                gabaI=(sc1i, sc2i),
                                                main=1,
                                                stim_param=stim_param,
                                                tstop=t_total,
                                                v_init=SAC_v_init)
        nspk.append(apcount.n)
        res_i = np.hstack([exc, gaba, ang, apcount.n, np.hstack(res_i)])
        res.append(res_i)
    res_dsi.append(np.hstack([exc,
                              gaba,
                              o,
                              of,
                              s.tl.DSI(angles, nspk),
                              s.tl.DSI(angles, nspk, ref_angle=180)]))
    print "Time elapsed: ", time.time() - start_time, "s"
    np.savetxt(simPath +
               synapse_type +
               '_%s_%s_%s_gabamax_data%s_heat-grande_%s_array%s.txt' %
               (s.amac_rec[0], s.amac_rec[1],
                s.amac_rec[2], s.dataidx,
                s.today,
                param_num),
               np.array(res),
               fmt='%6g', delimiter=',', header=head)
    np.savetxt(simPath +
               synapse_type +
               '_data_%s_date_%s_array_%s_dsi.txt' %
               (s.dataidx,
                s.today,
                param_num),
               np.array(res_dsi),
               fmt='%6g', delimiter=',', header=head_dsi)
    param_set = {'Excitation': exc,
                 'Inhibition': gaba,
                 'Overlap threshold': o,
                 'Overlap factor': of}
    # Parameters
    params_dict = dict()
    params_dict.update(param_set)
    params_dict.update(grid)
    params_dict.update(s.all_params)
    io.save_params_json(simPath +
                        synapse_type +
                        '_simulation_parameters_%s_%s.json' %
                        (s.today, param_num), params_dict)

if len(PARAM_NUMBER) > 1:
    np.savetxt(simPath +
               synapse_type +
               '_%s_%s_%s_gabamax_data%s_heat-grande_%s_all.txt' %
               (s.amac_rec[0], s.amac_rec[1],
                s.amac_rec[2], s.dataidx,
                s.today),
               np.array(res),
               fmt='%6g', delimiter=',', header=head)
