from __future__ import division
import json
import numpy as np
import os
import SACnetwork as s
import iodef as io

sc1i, sc2i = io.load_gabaInit_file('./gabaInit.json')

Gmax = (1e-5, 1e-4, 1e-3)
ldend = 123.65

mask_center = ((273.72, 212.25),
               (273.72 + ldend, 212.25),
               (273.72 + ldend / 2, 212.25),
               (273.72, 212.25),
               (273.72 - ldend / 2, 212.25),
               (273.72 - ldend, 212.25),
               (273.72 + 2 * ldend, 212.25))
mask_diam = (ldend * 2, ldend, ldend, ldend, ldend, ldend, ldend)
ind = range(0, len(mask_diam))

gind = 1
for g in Gmax:
    simPath = "./results_gmax%d/" % gind
    gind += 1

    if not os.path.exists(simPath):
        os.makedirs(simPath)
    for c, d, i in zip(mask_center, mask_diam, ind):
        s.stim_param['mask_center'] = c
        s.stim_param['mask_diam'] = d

        res, amac_vecs, synapse_vecs = s.main(gabaI=(sc1i, sc2i),
                                              main=1, excmax=g)

        with open(simPath + 'param_sim%d.json' %
                  i, 'w') as fp:
            json.dump(s.all_params, fp)

        for k in range(len(amac_vecs)):
            for j in range(len(amac_vecs[k])):
                np.savetxt(simPath +
                           "amac_vecs_sim%d_%d_%d.txt" % (i, k, j),
                           amac_vecs[k][j])

        for k in range(len(synapse_vecs)):
            for j in range(len(synapse_vecs[k])):
                np.savetxt(simPath +
                           "syn_vecs_sim%d_%d_%d.txt" % (i, k, j),
                           synapse_vecs[k][j])

        np.savetxt(simPath + "results_sim%d.txt" % i, res)
