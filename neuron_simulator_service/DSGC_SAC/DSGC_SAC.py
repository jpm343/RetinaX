# -*- coding: utf-8 -*-
"""

@author: Leo Medina
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
# folders...
this_file_path = str(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(str(this_file_path + '/../SAC_network'))
import SACnetwork as s
import iodef as io

# Stimulus parameters #########################################################
t_inf = s.t_es
stimulus_type = "bar"
stim_param = {'bar_speed': 1,      # stim speed [um/ms]
              'bar_width': 400,     # stimuli width [um]
              'bar_x_init': 0,     # bar initial position [um]
              'bar_angle': 0}      # angle of normal w/r to x-axis

# Simulation parameters #######################################################
sampinvl = 0.1

# BP parameters ###############################################################
synapse_type = "BPexc"
excGmax = 1e-4
excGmin = 0
SAC_excGmax = 1e-4
tau = (2, 10)  # rise and decay times

# Gabaergic function ##########################################################
k1 = 2
k2 = 0.8
th1 = -40
th2 = 0.8
e_rev = -75
gabaGmin = 0  # 0.0005
gabaGmax = 1e-3  # 0.8
pref_dend = 0  # SAC dendrite # for direction selectivity
null_dend = 2  # SAC dendrite # for direction selectivity
release_seg = 0.95  # [0,1] as in NEURON convention; near 1 for tip
is_symmetric = False  # True:All SAC dendrite to DSGC. False:Only preferred

# Ganglion cell parameters ####################################################
dsgc_type = 'DSGC2'
dsgc_rad = 100
dsgc_x = 300  # 200
dsgc_y = 250  # 120
dsgc_ndend = 4

# NEURON parameters ###########################################################
tstop = 1000  # sim time
v_init = -75
v_init_axon = -80
SAC_v_init = -60  # initial membrane voltage of DSGC
s.h.cvode.atol(1e-3)

if os.path.exists('./DSGC-SAC.json'):
    io.load_params_json('./DSGC-SAC.json', globals())

# Initialize DSGC
if os.getcwd() != this_file_path:  # if same, loaded at importing h
    s.load_mechanisms(this_file_path)  # load additional mechanisms
if dsgc_type == 'DSGC':
    s.h.load_file(str(this_file_path + '/DSGC.hoc'))
    dscell = s.h.DSGC(dsgc_rad, dsgc_x, dsgc_y, 3, 1.5)
if dsgc_type == 'DSGC2':
    s.h.load_file(str(this_file_path + '/DSGC2.hoc'))
    dscell = s.h.DSGC2(dsgc_rad, dsgc_x, dsgc_y, 3, 1.5)
elif dsgc_type == 'DSGC_Poleg':
    s.h.load_file(str(this_file_path + '/RGCmodel.hoc'))
    dscell = s.h.DSGC_Poleg(dsgc_x, dsgc_y, 0)
dscell.setv(v_init, v_init, v_init_axon)  # set initial votage

# BP cell - DSGC synapses
gBPsyn = []

# SAC - DSGC synapses
gSACsyn = []

# Recording vectors
timevec = s.h.Vector()
timevec.from_python(np.arange(0, tstop, sampinvl))
timerec = s.h.Vector()
timerec.record(s.h._ref_t, timevec)

if dsgc_type in ('DSGC', 'DSGC2'):
    dsgcV = [s.h.Vector(tstop / sampinvl) for i in range(7)]
    dsgcV[0].record(dscell.dend1[0](0.5)._ref_v, timevec)
    dsgcV[1].record(dscell.dend1[2](0.5)._ref_v, timevec)
    dsgcV[2].record(dscell.dend1[4](0.5)._ref_v, timevec)
    dsgcV[3].record(dscell.dend1[6](0.5)._ref_v, timevec)
    dsgcV[4].record(dscell.soma(0.75)._ref_v, timevec)
    dsgcV[5].record(dscell.axon(0.07)._ref_v, timevec)
    dsgcV[6].record(dscell.axon(0.99)._ref_v, timevec)
elif dsgc_type == 'DSGC_Poleg':
    dsgcV = [s.h.Vector(tstop / sampinvl) for i in range(5)]
    dsgcV[0].record(dscell.soma(0.75)._ref_v, timevec)
    dsgcV[1].record(dscell.dend[0](0.5)._ref_v, timevec)
    dsgcV[2].record(dscell.dend[20](0.5)._ref_v, timevec)
    dsgcV[3].record(dscell.dend[40](0.5)._ref_v, timevec)
    dsgcV[4].record(dscell.dend[60](0.5)._ref_v, timevec)


def bipolar_DSGC_synapses(s):

    for BPi in s.BPpos:
        if (np.sqrt((dsgc_x - BPi[0])**2 + (dsgc_y - BPi[1])**2) < dsgc_rad):
            angle = np.arctan2(BPi[1] - dsgc_y, BPi[0] - dsgc_x)
            if angle < 0:
                angle += 2 * np.pi
            if (np.sqrt((dsgc_x - BPi[0])**2 +
                        (dsgc_y - BPi[1])**2) < dsgc_rad / 2):
                ndend = int(angle * dsgc_ndend / (2 * np.pi) + 0.5)
                if ndend == dsgc_ndend:
                    ndend = 0
                raux = np.sqrt((BPi[0] - dsgc_x)**2 +
                               (BPi[1] - dsgc_y)**2) / dscell.dend0[0].L
                gBPsyn.append([getattr(s.h,
                                       synapse_type)(raux,
                                                     sec=dscell.dend0[ndend]),
                               BPi[0], BPi[1], dsgc_rad / 2])
            else:
                ndend = int(angle / (np.pi / 4)) + 1
                if ndend == dsgc_ndend * 2:
                    ndend = 0
                raux = (np.sqrt((BPi[0] - dsgc_x)**2 +
                                (BPi[1] - dsgc_y) ** 2) -
                        dscell.dend0[0].L) / dscell.dend1[0].L
                gBPsyn.append([getattr(s.h,
                                       synapse_type)(raux,
                                                     sec=dscell.dend1[ndend]),
                               BPi[0], BPi[1], dscell.dend1[0].L])
            gBPsyn[-1].append(s.h.NetStim())
            gBPsyn[-1][-1].number = 0
            gBPsyn[-1].append(s.h.NetCon(gBPsyn[-1][-1], gBPsyn[-1][0]))
    return gBPsyn


def bipolar_DSGC_Poleg_synapses(s):
    rad_thresh = 12

    for sec in dscell.ON:
        about_mid = int(s.h.n3d(sec=sec) / 2)
        sec_x = s.h.x3d(about_mid, sec=sec)
        sec_y = s.h.y3d(about_mid, sec=sec)
        for BPi in s.BPpos:

            if (np.sqrt((sec_x - BPi[0])**2 +
                        (sec_y - BPi[1])**2) < rad_thresh):
                gBPsyn.append([getattr(s.h,
                                       synapse_type)(.5, sec=sec),
                               BPi[0], BPi[1], dsgc_rad / 2])
                gBPsyn[-1].append(s.h.NetStim())
                gBPsyn[-1][-1].number = 0
                gBPsyn[-1].append(s.h.NetCon(gBPsyn[-1][-1], gBPsyn[-1][0]))
    return gBPsyn


def SAC_DSGC_synapses(s, thresh=100, overlap_factor=1, sym=is_symmetric):
    SACsynpos = []
    synM = []
    amac_num = -1
    # thresh = 100  # area overlap threshold for establishing synapse
    trick_nseg = 3  # trick for using overlap function of SAC-SAC connections
    xsyn = 0.5  # where in segment to introduce GABA synapse
    if sym:
        which_sac_dend = (pref_dend, pref_dend + 1, null_dend, null_dend + 1)
        print "Symmetric SAC-DSGC connectivity"
    else:
        which_sac_dend = (pref_dend,)
        print "Preferred side SAC-DSGC connectivity"
    theta2 = (np.pi / 8 +
              np.arcsin(np.sin(np.pi / 8) /
                        np.sqrt(5 - 4 * np.cos(np.pi / 8))))
    for amac in s.amac:
        amac_num += 1
        amac_x = s.h.x3d(0, sec=amac.soma)
        amac_y = s.h.y3d(0, sec=amac.soma)
        soma_to_soma = np.sqrt((dsgc_x - amac_x)**2 + (dsgc_y - amac_y)**2)
        # and dsgc_x > amac_x):
        if (soma_to_soma < dsgc_rad + amac.dend[pref_dend].L):
            idend = -1
            for dend in dscell.dend0:
                idend += 1
                for adend in which_sac_dend:
                    olap = s.topo.overlap(dsgc_x, amac_x, dsgc_y, amac_y,
                                          trick_nseg * dend.L,
                                          amac.dend[adend].L, dsgc_ndend,
                                          idend, adend,
                                          trick_nseg,
                                          amac.dend[adend].nseg,
                                          0,  # dends in dend0-->1st seg trick
                                          int(release_seg *
                                              amac.dend[adend].nseg))
                    olap = olap * overlap_factor  # scale area 4 syn weight
                    if olap > thresh:
                        angle = idend * np.pi / 2
                        gSACsyn.append(s.h.GABAsyn(xsyn, sec=dend))
                        s.h.setpointer(amac.dend[adend](release_seg)._ref_v,
                                       'vpre', gSACsyn[-1])
                        SACsynpos.append((dsgc_x +
                                          xsyn * dend.L * np.cos(angle),
                                          dsgc_y +
                                          xsyn * dend.L * np.sin(angle)))
                        synM.append((0, amac_num, idend, adend,
                                     int(xsyn * dend.nseg),
                                     int(release_seg * amac.dend[adend].nseg),
                                     olap))
            idend = -1
            for dend in dscell.dend1:
                idend += 1
                for adend in which_sac_dend:
                    olap = s.topo.overlap2(dsgc_x, amac_x, dsgc_y, amac_y,
                                           trick_nseg *
                                           dscell.dend0[int(idend / 2)].L,
                                           amac.dend[adend].L, dsgc_ndend,
                                           idend, adend,
                                           trick_nseg,
                                           amac.dend[adend].nseg,
                                           1,  # dends in dend1-->2nd seg trick
                                           int(release_seg *
                                               amac.dend[adend].nseg))
                    olap = olap * overlap_factor  # scale area 4 syn weight
                    if olap > thresh:
                        gSACsyn.append(s.h.GABAsyn(xsyn, sec=dend))
                        s.h.setpointer(amac.dend[adend](release_seg)._ref_v,
                                       'vpre', gSACsyn[-1])
                        theta1 = int(idend / 2) * 2 * np.pi / dsgc_ndend
                        lparent = dscell.dend0[int(idend / 2)].L
                        xpos = (dsgc_x +
                                lparent * np.cos(theta1) +
                                xsyn * dend.L * np.cos(theta2) *
                                np.sign(np.cos(idend *
                                               np.pi / 4 - np.pi / 16)))
                        ypos = (dsgc_y +
                                lparent * np.sin(theta1) +
                                xsyn * dend.L * np.sin(theta2) *
                                np.sign(np.sin(idend *
                                               np.pi / 4 - np.pi / 16)))
                        SACsynpos.append((xpos, ypos))
                        synM.append((0, amac_num, dsgc_ndend + idend, adend,
                                     int(xsyn * dend.nseg),
                                     int(release_seg * amac.dend[adend].nseg),
                                     olap))
    return np.array(SACsynpos), np.array(synM)


def SAC_DSGC_Poleg_synapses(s):
    rad_thresh = 15
    SACsynpos = []
    synM = []
    for sec in dscell.ON:
        about_mid = int(s.h.n3d(sec=sec) / 2)
        sec_x = s.h.x3d(about_mid, sec=sec)
        sec_y = s.h.y3d(about_mid, sec=sec)
        for amac in s.amac:
            tipx = s.h.x3d(0, sec=amac.soma) + amac.dend[pref_dend].L
            tipy = s.h.y3d(0, sec=amac.soma)
            dist_to_tip = np.sqrt((sec_x - tipx)**2 + (sec_y - tipy)**2)
            if (dist_to_tip < rad_thresh):
                gSACsyn.append(s.h.GABAsyn(.5, sec=sec))
                s.h.setpointer(amac.dend[pref_dend](release_seg)._ref_v,
                               'vpre', gSACsyn[-1])
                SACsynpos.append((sec_x, sec_y))
                #  The following is to get a matrix as in SACnetwork
                synM.append((0, 0, 0, 0, 0, 0,
                             1200 * dist_to_tip / (rad_thresh / 4.)))
                break  # SAC will make synapse to only one DSGC section
    return np.array(SACsynpos), np.array(synM)


def insert_soma_stim(amp=1, dur=tstop, delay=0):
    istim = s.h.IClamp(.5, sec=dscell.soma)  # In the middle of soma
    istim.amp = amp
    istim.dur = dur
    istim.delay = delay

    return istim


if __name__ == "__main__":
    # Setting DSGC inputs #####################################################
    # This is for DSGC inputs. Note that SAC syanpses are set and defined in
    # SAC_network
    if dsgc_type in ('DSGC', 'DSGC2'):
        gBPsyn = bipolar_DSGC_synapses(s)
        GABAsynpos, synM = SAC_DSGC_synapses(s)
    elif dsgc_type == 'DSGC_Poleg':
        gBPsyn = bipolar_DSGC_Poleg_synapses(s)
        GABAsynpos, synM = SAC_DSGC_Poleg_synapses(s)
    gBPsyn = s.topo.excGset(gBPsyn, gmax=excGmax, gmin=excGmin,
                            synapse_type=synapse_type, tau=tau)
    s.stim.set_stimulus(gBPsyn, stimulus_type, t_inf, synapse_type,
                        **stim_param)
    s.topo.gabaGset(gSACsyn, synM, gabaGmax, gabaGmin, k1, k2, th1, th2, e_rev)

    # Recording vectors #######################################################
    inh_synI = [s.h.Vector(tstop / sampinvl) for i in range(len(gSACsyn))]
    for (r, syn) in zip(inh_synI, gSACsyn):
        r.record(syn._ref_i, timevec)

    exc_synI = [s.h.Vector(tstop / sampinvl) for i in range(len(gBPsyn))]
    for (r, syn) in zip(exc_synI, gBPsyn):
        r.record(syn[0]._ref_i, timevec)

    vpre = [s.h.Vector(tstop / sampinvl) for i in range(len(gSACsyn))]
    for (r, syn) in zip(vpre, gSACsyn):
        r.record(syn._ref_vpre, timevec)

    sc2 = [s.h.Vector(tstop / sampinvl) for i in range(len(gSACsyn))]
    for (r, syn) in zip(sc2, gSACsyn):
        r.record(syn._ref_sc2, timevec)

    # ginh = [s.h.Vector(tstop / sampinvl) for i in range(len(gSACsyn))]
    # for (r, syn) in zip(ginh, gSACsyn):
    #     r.record(syn._ref_g, timevec)

    # iclamp = insert_soma_stim()
    # pt.bipolar_SAC_map(s, '', dscell, BPpos, GABAsynpos)
    res, amac_vecs, synapse_vecs = s.main(excmax=SAC_excGmax,
                                          gabaI=1, main=1,
                                          stim_param=stim_param,
                                          tstop=tstop, v_init=SAC_v_init)
    plt.figure()
    plt.subplot(111)
    for v in dsgcV:
        plt.plot(timerec, v)
    if dsgc_type in ('DSGC', 'DSGC2'):
        plt.legend(('dend1[0]', 'dend1[2]', 'dend1[4]',
                    'dend1[6]', 'soma', 'AIS', 'axon'), loc='best')
    elif dsgc_type == 'DSGC_Poleg':
        plt.legend(('soma', 'dend[0]', 'dend[20]', 'dend[40]',
                    'dend[60]'), loc=7)
    plt.xlabel('Time (ms)')
    plt.ylim((-80, -30))
    # plt.subplot(212)
    # for a in dsgcA:
    #    plt.plot(timerec,a)
    # plt.legend(('m_soma','h_soma','m_AIS','h_AIS'))
    plt.figure()
    plt.subplot(311)
    plt.title('Synapse #59')
    plt.plot(timevec, vpre[59])
    plt.ylim((-65, -40))
    plt.ylabel('$V_{SAC}$')
    plt.subplot(312)
    g = gSACsyn[59].minG + (
        gSACsyn[59].maxG - gSACsyn[59].minG) * sc2[59].as_numpy()
    i2 = g * (dsgcV[0].as_numpy() - e_rev)
    plt.plot(timevec, i2, timevec, inh_synI[59])
    plt.ylabel('$I_{inh}$')
    plt.ylim((0, 1e-2))
    plt.subplot(313)
    plt.plot(timevec, g)
    plt.ylabel('$g_{inh}$')
    plt.ylim((0, 1e-2))
    plt.xlabel('Time (ms)')
