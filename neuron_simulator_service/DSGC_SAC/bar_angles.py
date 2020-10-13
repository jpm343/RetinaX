from __future__ import division
import numpy as np
from DSGC_SAC import *


# Parameters ##################################################################
n_angles = 4  # Number of angles to plot
nsyn = 8  # Synaptic connection to plot (see synM)
tstop = 1000  # Simulation duration
SAC_excGmax = 4.25e-5  # Stim amplitude (G_max excitatory) for SACs
bar_speed = 1.61
excGmax = 1 * SAC_excGmax  # Stim amplitude for DSGC; note factor
gabaGmax = 0.46 * s.gabaGmax  # Inhibitory weight w/r to SAC
olap_thresh = 1000  # Threshold of overlap area for SAC/DSGC connection
ofactor = 1  # Weight of overlap area for synapse
###############################################################################

diag = np.sqrt(dsgc_x ** 2 + dsgc_y ** 2)
if n_angles == 12:
    angles = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
    d_inits = (0, 0, 0, 0, 2 * dsgc_x, 2 * dsgc_x, 2 * dsgc_x, 2 * diag,
               2 * diag, 2 * dsgc_y, 2 * dsgc_y, 2 * dsgc_y)
    plot_indexs = (6, 3, 3, 2, 1, 1, 4, 7, 7, 8, 9, 9)
elif n_angles == 8:
    angles = (0, 45, 90, 135, 180, 225, 270, 315)
    d_inits = (0, 0, 0, diag, 2 * dsgc_x, 2 * diag, 2 * dsgc_y, diag)
    plot_indexs = (6, 3, 2, 1, 4, 7, 8, 9)
elif n_angles == 4:
    angles = (0, 180, 90, 270)
    d_inits = (0, 2 * dsgc_x, 0, 2 * dsgc_y)
    plot_indexs = (6, 4, 2, 8)
elif n_angles == 2:
    angles = (180, 0)
    d_inits = (2 * dsgc_x, 0)
    plot_indexs = (4, 6)
elif n_angles == 1:
    angles = (180, )
    d_inits = (2 * dsgc_x, )
    plot_indexz = (4, )

nspk = []
fig_v = plt.figure()
fig_s1 = plt.figure()
fig_s2 = plt.figure()
fig_s3 = plt.figure()

gBPsyn = bipolar_DSGC_synapses(s)
GABAsynpos, synM = SAC_DSGC_synapses(s,
                                     thresh=olap_thresh,
                                     overlap_factor=ofactor)

for (ang, d_init, plti) in zip(angles[::-1], d_inits[::-1], plot_indexs[::-1]):
    stim_param['bar_x_init'] = d_init
    stim_param['bar_angle'] = ang
    stim_param['bar_speed'] = bar_speed
    # Setting DSGC inputs #####################################################
    # This is for DSGC inputs. Note that SAC syanpses are set and defined in
    # SAC_network
    dscell.setv(-75.5, -75.5, -79)
    gBPsyn = s.topo.excGset(gBPsyn, gmax=excGmax, gmin=excGmin,
                            synapse_type=synapse_type, tau=tau)
    s.stim.set_stimulus(gBPsyn, stimulus_type, t_inf, synapse_type,
                        **stim_param)
    s.topo.gabaGset(gSACsyn, synM, gabaGmax, gabaGmin, k1, k2, th1, th2, e_rev)

    # Recording vectors #######################################################
    timevec = s.h.Vector()
    timevec.from_python(np.arange(0, tstop, sampinvl))
    timerec = s.h.Vector()
    timerec.record(s.h._ref_t, timevec)
    dsgcV = [s.h.Vector(tstop / sampinvl) for i in range(7)]
    dsgcV[0].record(dscell.dend1[0](0.5)._ref_v, timevec)
    dsgcV[1].record(dscell.dend1[2](0.5)._ref_v, timevec)
    dsgcV[2].record(dscell.dend1[4](0.5)._ref_v, timevec)
    dsgcV[3].record(dscell.dend1[6](0.5)._ref_v, timevec)
    dsgcV[4].record(dscell.soma(0.75)._ref_v, timevec)
    dsgcV[5].record(dscell.axon(0.07)._ref_v, timevec)
    dsgcV[6].record(dscell.axon(0.99)._ref_v, timevec)

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

    apcount = s.h.APCount(dscell.axon(.9))

    # ginh = [s.h.Vector(tstop / sampinvl) for i in range(len(gSACsyn))]
    # for (r, syn) in zip(ginh, gSACsyn):
    #     r.record(syn._ref_g, timevec)

    # iclamp = insert_soma_stim()
    # pt.bipolar_SAC_map(s, '', dscell, BPpos, GABAsynpos)
    res, amac_vecs, synapse_vecs = s.main(excmax=SAC_excGmax,
                                          gabaI=1, main=1,
                                          stim_param=stim_param,
                                          tstop=tstop, v_init=SAC_v_init)
    nspk.append(apcount.n)

    plt.figure(fig_v.number)
    plt.subplot(3, 3, plti)
    pltleg = 8
    for v in dsgcV:
        plt.plot(timerec, v)
    if plti == pltleg:
        if dsgc_type in ('DSGC', 'DSGC2'):
            plt.legend(('dend1[0]', 'dend1[2]', 'dend1[4]',
                        'dend1[6]', 'soma', 'AIS', 'axon'), loc='best')
        elif dsgc_type == 'DSGC_Poleg':
            plt.legend(('soma', 'dend[0]', 'dend[20]', 'dend[40]',
                        'dend[60]'), loc=7)
        plt.xlabel('Time (ms)')
        plt.ylabel('Transmembrane Voltage (mV)')
    plt.ylim((-80, -30))
    # plt.subplot(212)
    # for a in dsgcA:
    #    plt.plot(timerec,a)
    # plt.legend(('m_soma','h_soma','m_AIS','h_AIS'))
    plt.figure(fig_s1.number)
    plt.subplot(3, 3, plti)
    if plti == pltleg:
        plt.title('GABA Synapse #' + str(nsyn))
        plt.ylabel('Preterminal Voltage (mV)')
        plt.xlabel('Time (ms)')
    plt.plot(timevec, vpre[nsyn])
    plt.ylim((-65, -40))

    for ns in range(0, len(gSACsyn)):
        plt.figure(fig_s2.number)
        plt.subplot(3, 3, plti)
        g = gSACsyn[ns].minG + (
            gSACsyn[ns].maxG - gSACsyn[ns].minG) * sc2[ns].as_numpy()
        i2 = g * (dsgcV[0].as_numpy() - e_rev)
        plt.plot(timevec, 1000 * i2, timevec, 1000 * exc_synI[nsyn].as_numpy())
        if plti == pltleg:
            plt.title('GABA Synapse #' + str(nsyn))
            plt.ylabel('Synaptic Current ($\mu$A)')
            plt.xlabel('Time (ms)')
        # plt.ylim((0, .20))

        plt.figure(fig_s3.number)
        plt.subplot(3, 3, plti)
        plt.plot(timevec, g * 1000)
        if plti == pltleg:
            plt.title('GABA synapse #' + str(nsyn))
            plt.ylabel('Synaptic Conductance (mS)')
            plt.xlabel('Time (ms)')
        # plt.ylim((0, .150))

dsi = s.tl.DSI(angles, nspk)
