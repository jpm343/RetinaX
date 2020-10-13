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
G_MIN_EXP = -6
G_MAX_EXP = -3
G_NUMBER = 20
VELOC_MIN_EXP = -1
VELOC_MAX_EXP = 2
VELOC_NUMBER = 20
PARAM_NUMBER = sys.argv[1]
diag = np.sqrt(250 ** 2 + 300 ** 2)
angles = (0, 45, 90, 135, 180, 225, 270, 315)
d_inits = (0, 0, 0, diag, 2 * dsgc_x, 2 * diag, 2 * dsgc_y, diag)
# Factors determined by simulations:
excfactor = 3.6  # factor of excitation (times of BP excitation on SAC)
inhfactor = 0.46  # factor of inhibition (times of SAC-SAC inhibition)
overlap_thresh = 500  # threshold for area overlap in SAC-DSGC synapse
olap_factor = 1  # Multiplies the overlap area
###############################################################################


if os.path.exists('./array-DSGC-SAC.json'):
    io.load_params_json('./array-DSGC-SAC.json', globals())
if os.path.exists('./gabaInit.json'):
    print "Loading GABA initial parameters from file..."
    sc1i, sc2i = io.load_gabaInit_file('./gabaInit.json')
else:
    sc1i, sc2i = s.gabaInit(s.excGmin)

gmax = np.logspace(G_MIN_EXP, G_MAX_EXP, G_NUMBER)
stimuliSpeed = np.logspace(VELOC_MIN_EXP, VELOC_MAX_EXP, VELOC_NUMBER)
synapse_type = s.synapse_type  # Note this param is in SACnetwork.py
params = [(g, v) for g in gmax for v in stimuliSpeed]

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

head = 'speed,gmax,angle,nspk,width,speed1,' + ','.join(head_entries)
head_dsi = 'speed,gmax,dsi,dsi_angle180'

grid = {'Initial speed': stimuliSpeed[0],
        'Final Speed': stimuliSpeed[-1],
        'Speed points': len(stimuliSpeed),
        'Initial conductance': gmax[0],
        'Final conductance': gmax[-1],
        'Conductance points': len(gmax)}

if not isinstance(PARAM_NUMBER, list):
    PARAM_NUMBER = [PARAM_NUMBER]

res = []
res_dsi = []
for param_num in PARAM_NUMBER:
    g, sp = params[int(param_num)]
    print "Running sim with speed %f and max conductance %f" % (sp, g)
    # Assuming a field of about 1 mm, simulation must be long enough for bar to
    # cover the entire field. sp in mm/s, multiply by 1000 to convert to ms
    t_total = s.t_es + (1.0 +
                        s.stim_param['bar_width'] /
                        1000.0) / sp * 1000.0
    if t_total < 1500:
        t_total = 1500  # Sim no shorter than 1.5 s, see calculation of DSI
    s.tstop = t_total
    gBPsyn = bipolar_DSGC_synapses(s)
    GABAsynpos, synM = SAC_DSGC_synapses(s, thresh=overlap_thresh,
                                         overlap_factor=olap_factor,
                                         sym=is_symmetric)
    nspk = []
    for (ang, d_init) in zip(angles, d_inits):
        stim_param['bar_x_init'] = d_init
        stim_param['bar_angle'] = ang
        stim_param['bar_speed'] = sp
        # Setting DSGC inputs ################################################
        # This is for DSGC inputs. Note that SAC syanpses are set and defined
        # SAC_network
        dscell.setv(v_init, v_init, v_init_axon)
        gBPsyn = s.topo.excGset(gBPsyn, gmax=excfactor * g, gmin=excGmin,
                                synapse_type=synapse_type, tau=tau)
        s.stim.set_stimulus(gBPsyn, stimulus_type, t_inf, synapse_type,
                            **stim_param)
        s.topo.gabaGset(gSACsyn, synM, inhfactor * s.gabaGmax, gabaGmin,
                        k1, k2, th1, th2, e_rev)

        apcount = s.h.APCount(dscell.axon(.9))

        res_i, amac_vecs, synapse_vecs = s.main(excmax=g,
                                                gabaI=(sc1i, sc2i),
                                                main=1,
                                                stim_param=stim_param,
                                                tstop=t_total,
                                                v_init=SAC_v_init)
        nspk.append(apcount.n)
        res_i = np.hstack([sp, g, ang, apcount.n, np.hstack(res_i)])
        res.append(res_i)
    res_dsi.append(np.hstack([sp,
                              g,
                              s.tl.DSI(angles, nspk),
                              s.tl.DSI(angles, nspk, ref_angle=180)]))
    print "Time elapsed: ", time.time() - start_time, "s"
    np.savetxt(simPath +
               synapse_type +
               '_%s_%s_%s_gmax_data%s_heat-grande_%s_array%s.txt' %
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
    param_set = {'Speed': sp,
                 'Conductance': g}
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
               '_%s_%s_%s_gmax_data%s_heat-grande_%s_all.txt' %
               (s.amac_rec[0], s.amac_rec[1],
                s.amac_rec[2], s.dataidx,
                s.today),
               np.array(res),
               fmt='%6g', delimiter=',', header=head)
