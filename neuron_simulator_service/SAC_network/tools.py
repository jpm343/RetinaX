# import topology as topo
import numpy as np
import glob
import pandas as pd


# Direction selectivity index for a spiking cell like DSGC
def DSI(angles, nspk, ref_angle=None):
    # angles: the angles of the applied stimuli
    # nspk: number of spikes obtained for the applied angles
    # ref_angle: reference angle to obtain DSI for a particular direction

    DSIx = 0
    DSIy = 0
    ntot = 0
    for (ang, n) in zip(angles, nspk):
        DSIx += n * np.cos(np.deg2rad(ang))
        DSIy += n * np.sin(np.deg2rad(ang))
        ntot += n
    if ntot == 0:
        # no selectivity if no spike
        return 0
    if ref_angle is not None:
        # DSI w/r a reference angle
        # The following rotates (DSIx,DSIy) and gets the DSIx of
        # the rotated axes
        ref_angle = np.deg2rad(ref_angle)
        return (DSIx * np.cos(ref_angle) - DSIy * np.sin(ref_angle)) / ntot
    return np.linalg.norm((DSIx, DSIy)) / ntot


# Direction selectivity index
def DS(t_es, nullvec, prefvec, sampinvl, area=0):
    init_idx = int(t_es / sampinvl)  # Time step
    end_idx = len(nullvec) - 1
    if area == 1:  # Calcula area bajo la curva
        resp_pref = sum(prefvec[init_idx:end_idx]) / (end_idx - init_idx)
        resp_null = sum(nullvec[init_idx:end_idx]) / (end_idx - init_idx)
        base_pref = sum(prefvec[init_idx - 10:init_idx]) / 10
        base_null = sum(nullvec[init_idx - 10:init_idx]) / 10
    else:  # Calcula DSI
        resp_pref = max(prefvec[init_idx:])
        resp_null = max(nullvec[init_idx:])
        base_pref = np.mean(prefvec[init_idx - 50:init_idx])
        base_null = np.mean(nullvec[init_idx - 50:init_idx])
    return [resp_pref - base_pref,
            ((resp_pref - base_pref) - (resp_null - base_null)) /
            ((resp_pref - base_pref) + (resp_null - base_null))]


def return_syn_rec(amac_rec, synM, pref_dend=0, null_dend=2):
    syn_rec = []
    for amac in amac_rec:
        a = np.where((synM[:, 0] == amac) & (synM[:, 2] == null_dend))[0][0]
        b = np.where((synM[:, 0] == amac) & (synM[:, 2] == pref_dend))[0][0]
        syn_rec.append((a, b))
    return syn_rec


def make_dictionary(**kwargs):
    d = dict((name, value) for name, value in kwargs.iteritems())
    return d


def gather_results_array_job(folder, ext='.txt'):
    filelist = glob.glob(folder + '*' + ext)
    s = []
    print "Gathering result files..."
    for f in filelist:
        r = f.replace(ext, '').split('_')[-1]
        s.append(int(''.join(x for x in r if x.isdigit())))
    rootstr = f.split('_array')[0] + '.txt'
    # sort filelist by array number
    filelist = [filelist[s.index(i)] for i in range(len(s))]
    df = pd.DataFrame()
    for f in filelist:
        df = df.append(pd.read_csv(f))
    df.to_csv(rootstr)
    return rootstr
