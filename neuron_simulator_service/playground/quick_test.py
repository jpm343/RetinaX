import sys
import numpy as np

sys.path.append('../repo/SAC_network')

import SACnetwork as s

sc1i, sc2i = s.gabaInit(s.excGmin)
s.stim_param['bar_speed'] = 3
res, amac_vecs, synapse_vecs = s.main(gabaI=(sc1i, sc2i), excmax=1e-4, main=1)

np.savetxt("results.txt", res)

for k in range(len(amac_vecs)):
        for j in range(len(amac_vecs[k])):
            np.savetxt("amac_vecs%d_%d.txt" % (k, j),
                       amac_vecs[k][j])

for k in range(len(synapse_vecs)):
    for j in range(len(synapse_vecs[k])):
        np.savetxt("syn_vecs%d_%d.txt" % (k, j),
                   synapse_vecs[k][j])
