from __future__ import division
import numpy as np
from neuron import h
import random as rd


def load_SAC_topology(celldata, ndend, dendseg, diam_min, diam_max):
    amac = [h.SAC(ndend, celld[2], celld[0], celld[1],
                  dendseg, diam_min, diam_max) for celld in celldata]
    print len(amac), " Starburst Amacrine Cells created"
    return amac


def create_bipolar_map(celldata, d_is, is_random=False):
    BPpos = []  # Glutamatergic (bipolar) input position

    # Position of the SAC's dendrites in the network
    xmin = min(celldata[:, 0] - celldata[:, 2])
    xmax = max(celldata[:, 0] + celldata[:, 2])
    ymin = min(celldata[:, 1] - celldata[:, 2])
    ymax = max(celldata[:, 1] + celldata[:, 2])
    '''
    If at point (x,y) a displacement within a circle with a random radius 'a',
    and a random direction angle 'b' is smaller than ldend, the point is stored
    in BPos. These vectors store the coords where we will place the synaptic
    input
    '''
    a = 0  # If not random
    b = 0
    y = ymin
    row = 0
    while (y <= ymax):
        x = xmin + (1 + (-1) ** row) * d_is / 4
        while (x <= xmax):  # i-th somatic position
            if is_random:
                a = np.random.normal(loc=0, scale=np.sqrt(2))
                b = np.random.uniform(low=0, high=2 * np.pi)
            BPpos.append([x + a * np.cos(b), y + a * np.sin(b)])
            x += d_is
        y += d_is * np.sin(np.pi / 3)
        row += 1
    print len(BPpos), " Bipolar Cells created"

    return BPpos


def bipolar_SAC_synapses(amac, BPpos, ndend, synapse_type="alphaCSyn",
                         dend_input_segments='all'):

    # Coupling Glutamatergic synapses to SACs
    # lets define the kind of glutamatergic synapse we want.
    # a) g = minG + (maxG - minG)*sin(3.14159*( t -onset)/dur) <-- 'fullWave'
    # b) alpha function convolved with rectangular pulse <-- 'convolution'
    BPsyn = []
    for SACi in amac:
        x0 = h.x3d(1, sec=SACi.soma)       # i-th soma, x position
        y0 = h.y3d(1, sec=SACi.soma)       # i-th soma, y position
        L = SACi.dend[0].L  # assuming equal for all dendrites in SACi
        nseg = SACi.dend[0].nseg
        if dend_input_segments == 'all':
            dend_input_segments = range(0, nseg)
        for BPi in BPpos:
            dist = np.sqrt((x0 - BPi[0]) ** 2 + (y0 - BPi[1]) ** 2)
            raux = dist / L  # synapse to be inserted in this pos along dend
            the_seg = int(raux * nseg)
            if (dist < L and the_seg in dend_input_segments):
                angle = np.arctan2(BPi[1] - y0, BPi[0] - x0)
                if angle < 0:
                    angle += 2 * np.pi
                numdend = int(angle * ndend / (2 * np.pi) + 0.5)
                if numdend == ndend:
                    numdend = 0
                # creation of the synapse between SAC and bipolar
                BPsyn.append([getattr(h,
                             synapse_type)(raux, sec=SACi.dend[numdend]),
                              BPi[0], BPi[1], SACi.dend[numdend].L, the_seg])
                if synapse_type in ("Exp2Syn", "BPexc"):
                    BPsyn[-1].append(h.NetStim())
                    BPsyn[-1][-1].number = 0  # No stim by default
                    BPsyn[-1].append(h.NetCon(BPsyn[-1][-1], BPsyn[-1][0]))
    n_is = len(BPsyn)  # Ammount of glutamatergic synaptic inputs.
    print n_is, "Glutamatergic synaptic inputs created"

    return BPsyn, amac


# Set excitatory(glutamate) conductance
def excGset(BPsyn, gmax, gmin, synapse_type="alphaCSyn", tau=2):

    if synapse_type in ("alphaCSyn", "expCSyn", "BPexc"):
        for BPi in BPsyn:
            BPi[0].maxG = gmax
            BPi[0].minG = gmin
            BPi[0].dur = 0  # No activation by default
            if synapse_type in ("alphaCSyn", "expCSyn"):
                BPi[0].tau = tau
            if synapse_type == "BPexc":
                BPi[-2].number = 0  # No activation by default
                if type(tau) == tuple:
                    BPi[0].tau1 = tau[0]
                    BPi[0].tau2 = tau[1]
    elif synapse_type == "Exp2Syn":
        for BPi in BPsyn:
            BPi[-1].weight[0] = gmax
            BPi[-2].number = 0  # No activation by default
    else:
        print "Synapse: %s undefined!" % synapse_type

    return BPsyn


def load_gabaergic_data(synM, amac, dendseg):
    # Load gabaergic data
    gabasyn = []
    n_gsyn = len(synM)  # Gabaergic synaptic inputs
    print n_gsyn, "Gabaergic synaptic inputs"
    # Parameters for GABA synapsis
    # Lateral inhibition????
    for row in range(n_gsyn):
        cell1, cell2, dend1, dend2, seg1, seg2, olap = synM[row].astype(int)
        olap = float(olap)
        gabasyn.append(h.GABAsyn((seg2 + 0.5) / dendseg,
                                 sec=amac[cell2].dend[dend2]))
    #    gabasyn[row].minG = gabaGmin*olap / 5000
    #    gabasyn[row].maxG = gabaGmax*olap / 5000
        h.setpointer(amac[cell1].dend[dend1](
            (seg1 + 0.5) / dendseg)._ref_v, 'vpre', gabasyn[row])

    print "Gabaergic synaptic inputs created"
    return gabasyn, amac


def gabaGset(gabasyn, synM, gmax, gmin, k1, k2, th1, th2, e_rev=-60):

    n_gsyn = len(synM)  # Gabaergic synaptic inputs
    for i in range(n_gsyn):
        olap = synM[i, 6]
        gabasyn[i].minG = gmin * olap / 1200
        gabasyn[i].maxG = gmax * olap / 1200
        gabasyn[i].k1 = k1
        gabasyn[i].k2 = k2
        gabasyn[i].th1 = th1
        gabasyn[i].th2 = th2
        gabasyn[i].e = e_rev
    return gabasyn


def overlap(x1, x2, y1, y2, ld1, ld2,
            ndend, idend1, idend2, nseg1, nseg2, iseg1, iseg2,
            dt=np.pi / 100, dr=1):
    '''Calculates the overlap between the two areas covered by two
    SAC model dendrite segments.
    Note the use of polar coordinate system, given the radial symmetry
    of the covered areas'''
    # Traslation. Soma of SAC 2, with respecto to soma SAC 1
    r0 = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    t0 = np.arctan2(y2 - y1, x2 - x1)

    if r0 >= (ld1 + ld2):  # Too far, it should not be overlap
        return 0

    sumarea = 0
    # The following is strongly model geometry dependent.
    # It was designed for two SACs with 4 dendrites, but it may work for two
    # SACs with more but same number of dendrites
    # polar limits of area 1
    r1_min = iseg1 * ld1 / nseg1
    r1_max = (iseg1 + 1) * ld1 / nseg1
    t1_min = (2 * idend1 - 1) * np.pi / ndend
    t1_max = (2 * idend1 + 1) * np.pi / ndend
    # polar limits of area 2
    r2_min = iseg2 * ld2 / nseg2
    r2_max = (iseg2 + 1) * ld2 / nseg2
    t2_min = (2 * idend2 - 1) * np.pi / ndend
    t2_max = (2 * idend2 + 1) * np.pi / ndend

    for t1 in np.arange(t1_min, t1_max + dt, dt):
        for r1 in np.arange(r1_min, r1_max + dr, dr):
            r2 = np.sqrt(r1 ** 2 + r0 ** 2 + 2 * r1 * r0 * np.cos(t0 - t1))
            t2 = np.arctan2(y1 - y2 + r1 * np.sin(t1),
                            x1 - x2 + r1 * np.cos(t1))  # [-pi,pi]
            if t2 < -np.pi / 4:
                t2 = t2 + 2 * np.pi  # to match range of t2min-max
            if (t2 > t2_min and t2 <= t2_max and
               r2 > r2_min and r2 <= r2_max):
                sumarea += r1 * dr * dt
    return sumarea


def overlap2(x1, x2, y1, y2, ld1, ld2,
             ndend, idend1, idend2, nseg1, nseg2, iseg1, iseg2,
             dt=np.pi / 100, dr=1):
    '''This function has a slight modification with respect to overlap, to
    account for geometry of DSGC2.hoc (and DSGC.hoc too!), in which dendrites
    branch out. It was designed for 2 branches per dendrite (see angles)'''

    # Traslation. Soma of cell 2, with respecto to soma cell 1
    soma_to_soma = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    x1p = x1 + ld1 / nseg1 * np.cos(np.floor(idend1 / 2) * np.pi / 2)
    y1p = y1 + ld1 / nseg1 * np.sin(np.floor(idend1 / 2) * np.pi / 2)
    r0 = np.sqrt((x1p - x2) ** 2 + (y1p - y2) ** 2)
    t0 = np.arctan2(y2 - y1p, x2 - x1p)

    if soma_to_soma >= (ld1 + ld2):
        return 0

    sumarea = 0
    # polar limits of segment 1
    r1_min = iseg1 * ld1 / nseg1
    r1_max = (iseg1 + 1) * ld1 / nseg1
    t1_min = np.floor((idend1 - 1) / 2) * np.pi / (ndend / 2)
    t1_max = np.floor((idend1 - 1) / 2 + 1) * np.pi / (ndend / 2)

    # polar limits of area 2
    r2_min = iseg2 * ld2 / nseg2
    r2_max = (iseg2 + 1) * ld2 / nseg2
    t2_min = (2 * idend2 - 1) * np.pi / ndend
    t2_max = (2 * idend2 + 1) * np.pi / ndend

    for t1 in np.arange(t1_min, t1_max + dt, dt):
        for r1 in np.arange(r1_min, r1_max + dr, dr):
            r2 = np.sqrt(r1 ** 2 + r0 ** 2 + 2 * r1 * r0 * np.cos(t0 - t1))
            t2 = np.arctan2(y1p - y2 + r1 * np.sin(t1),
                            x1p - x2 + r1 * np.cos(t1))  # [-pi,pi]
            if t2 < -np.pi / 4:
                t2 = t2 + 2 * np.pi  # to match range of t2min-max
            if (t2 > t2_min and t2 <= t2_max and
               r2 > r2_min and r2 <= r2_max):
                sumarea += r1 * dr * dt
    return sumarea


def anglewithin(anglex, anglemin, anglemax):
    """
    Checks if anglex is within anglemin and anglemax
    """
    if anglemin > anglemax:
        if anglex < anglemax:
            anglex += np.pi * 2
        anglemax += np.pi * 2

    return anglemin < anglex and anglex < anglemax


def create_synapse_matrix(amac, thresh=800, sac_sac_segments='all'):
    '''cell1, idend1, iseg1 --> Presynaptic
    iseg1 iterates just on 3 since outputs are restricted to distal segment
    cell2, idend2, iseg2 --> Postsynaptic
    thresh: if area overlap exceeds thresh, then a synapse is established
    '''
    print "Creating matrix of synaptic information..."
    synM = []
    # SAC-SAC synapses
    for ncell1 in range(len(amac)):  # over presynaptic cell
        x1 = h.x3d(1, sec=amac[ncell1].soma)
        y1 = h.y3d(1, sec=amac[ncell1].soma)
        ld1 = amac[ncell1].dend[0].L
        for ncell2 in range(len(amac)):  # over postsynaptic cell
            x2 = h.x3d(1, sec=amac[ncell2].soma)
            y2 = h.y3d(1, sec=amac[ncell2].soma)
            ld2 = amac[ncell2].dend[0].L
            if (np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < (ld1 + ld2) and
               ncell1 != ncell2):
                for idend1 in range(len(amac[ncell1].dend)):
                    # Only distal end for presynaptic cell:
                    iseg1 = amac[ncell1].dend[idend1].nseg - 1
                    for idend2 in range(len(amac[ncell2].dend)):
                        if sac_sac_segments == 'all':
                            sac_sac_segments = range(0,
                                                     amac[ncell2].
                                                     dend[idend2].nseg)
                        for iseg2 in sac_sac_segments:
                            olap = overlap(x1, x2, y1, y2,
                                           ld1, ld2, len(amac[ncell1].dend),
                                           idend1, idend2,
                                           amac[ncell1].dend[idend1].nseg,
                                           amac[ncell2].dend[idend2].nseg,
                                           iseg1, iseg2)
                            if (olap > thresh):
                                synM.append((ncell1,
                                             ncell2,
                                             idend1,
                                             idend2,
                                             iseg1,
                                             iseg2,
                                             olap))
    return np.reshape(synM, (len(synM), 7))  # 7 variables per row


def build_cell_data_from_matrix(amac):
    xvec = []
    yvec = []
    lvec = []
    for amaci in amac:
        xvec.append(h.x3d(0.25, sec=amaci.soma))
        yvec.append(h.y3d(0.25, sec=amaci.soma))
        lvec.append(amaci.dend[0].L)  # assuming dendrite of same length
    return np.stack((xvec, yvec, lvec), axis=1)


def create_cell_data(mean_ldend=120, std_ldend=20**.5, std_shift=20**.5,
                     nrow=10, ncol=10, seed=1):
    print "Creating celldata of SAC positions and dendrite lengths..."
    xvec = []
    yvec = []
    lvec = []
    rd.seed(seed)
    # SAC positions
    lag_x = mean_ldend / 2
    lag_y = np.sin(np.pi / 3) * mean_ldend / 2
    for i in range(nrow):
        for j in range(ncol):
            yvec.append(i * lag_y + rd.gauss(0, std_shift))
            xvec.append(j * lag_x + (1 + (-1) ** i) * lag_x / 4 +
                        rd.gauss(0, std_shift))
            lvec.append(rd.gauss(mean_ldend, std_ldend))
    return np.stack((xvec, yvec, lvec), axis=1)


def apply_spatiotemporal_synaptic_input(BPsyn,
                                        dend_input_segments,
                                        tau1, tau2):
    '''Modifies the time constants tau of synapses (originally designed
    for BPexc) to create a spatiotemporal distribution of synaptic inputs.
    '''

    if (len(tau1) != len(dend_input_segments) or
       len(tau2) != len(dend_input_segments)):
        print "Warning! Vectors tau1 and tau2 different length from nseg"

    for BPi in BPsyn:
        the_seg = BPi[4]  # segment where synapse was inserted
        if the_seg in dend_input_segments:
            BPi[0].tau1 = tau1[the_seg]
            BPi[0].tau2 = tau2[the_seg]

    return BPsyn
