import json
import numpy as np
import sys
import os

sys.path.append('../repo/SAC_network')

G_MIN_EXP = -6
G_MAX_EXP = -3
G_NUMBER = 20
PARAM_NUMBER = int(sys.argv[1])

import SACnetwork as s
import iodef as io

sc1i, sc2i = io.load_gabaInit_file('./gabaInit.json')

gmax = np.logspace(G_MIN_EXP, G_MAX_EXP, G_NUMBER)
g = gmax[PARAM_NUMBER]

inner = (25, 50, 75, 100, 125, 150, 200)
outer = (75, 100, 125, 150, 175, 200, 250)

simPath = "./results%d/" % PARAM_NUMBER

if not os.path.exists(simPath):
    os.makedirs(simPath)

soma = s.amac[s.amac_rec[0]].soma
v_clamp = s.gabasyn[0].e
for x in np.arange(1.0 / soma.nseg / 2, 1, 1.0 / soma.nseg):
    s.stim.insert_voltage_clamp(s.h,
                                soma, x, v_clamp, s.tstop)
for dend in s.amac[s.amac_rec[0]].dend:
    for x in np.arange(1.0 / dend.nseg / 2, 1, 1.0 / dend.nseg):
        s.stim.insert_voltage_clamp(s.h, dend, x, v_clamp, s.tstop)

for i, o in zip(inner, outer):
    s.stim_param['inner_diam'] = i
    s.stim_param['outer_diam'] = o

    res, amac_vecs, synapse_vecs = s.main(gabaI=(sc1i, sc2i), main=1, excmax=g)

    with open(simPath + 'param_in%d_out%d.json' %
              (i, o), 'w') as fp:
        json.dump(s.all_params, fp)

    for k in range(len(amac_vecs)):
        for j in range(len(amac_vecs[k])):
            np.savetxt(simPath +
                       "amac_vecs_in%d_out%d_%d_%d.txt" % (i, o, k, j),
                       amac_vecs[k][j])

    for k in range(len(synapse_vecs)):
        for j in range(len(synapse_vecs[k])):
            np.savetxt(simPath +
                       "syn_vecs_in%d_out%d_%d_%d.txt" % (i, o, k, j),
                       synapse_vecs[k][j])

    np.savetxt(simPath + "results_in%d_out%d.txt" % (i, o), res)
