# -*- coding: utf-8 -*-
"""
Created on May 10 2017

@author: Leo Medina, based on code by Pato Orio
"""

from __future__ import division
import os
import numpy as np
# import matplotlib.colors as colors
from neuron import h, load_mechanisms
import datetime
import iodef as io
import topology as topo
import tools as tl
import stimulus as stim


# Parameters
#
# AMACRINE CELLS ##############################################################
# nrow = 4 #SAC per row
# ncol = 5 #SAC per column
ndend = 4               # dendrites number
dendseg = 3             # dendrites segments
diam_min = 0.5          # min dendrite diameter
diam_max = 1.5          # max dendritic diam
dend_input_segments = (0, 1)  # (0,1,2) segments whith bipolar inputs
sac_sac_segments = (0, )  # segments whith sac inputs
pref_dend = 0           # assuming stim from left to right
null_dend = pref_dend + int(ndend / 2.0 + 0.5)  # opposite to preferred
area_thresh = 600       # threshold of area overlap for SAC-SAC synapse
# Gabaergic function
k1 = 2
k2 = 0.8
th1 = -40
th2 = 0.8
gabaGmin = 0.000005
gabaGmax = 0.0008
# BIPOLAR CELLS ###############################################################
d_is = 15               # mean distance between synaptic input
excGmax = 0.000001      # 0.00001 Max excitatory conductance 0.0000380
excGmin = 0.0000001     # Min excitatory conductance
synapse_type = "BPexc"
BPsyn_tau = (2, 10)     # Time constant of synapse
BPtau1 = (20, 2)        # Time constant of BPexc synapse
BPtau2 = (1000, 10)
is_spatiotemporal = True
# STIMULUS  ###################################################################
# If bar, you likely want to ensure it starts from where it'll activate all BPs
stimulus_type = "bar"
stim_param = {'bar_speed': 1,      # stim speed [um/ms]
              'bar_width': 400,     # stimuli width [um]
              'bar_x_init': 0}  # bar initial position [um]
t_es = 100              # stabilization time [ms]
# DATA I/O  ###################################################################
dataidx = 13             # which file do I wanna use?
# Define recording vectors
amac_rec = (44, 54, 65)
sec_rec = 'dend'  # must be item of SACtmp. If dend, will record both pref&null
x_rec = (0.8, )  # 0.8[0,1]in NEURON coords,where to record withtin sec
var_amac_rec = ['v']    # variable to record in neuron section. Must be list!
var_syn_rec = ['sc2']   # variable to record in synapse. Must be list!
# NEURON  #####################################################################
# If stim is moving bar, you likely want to ensure simulation time is long
# enough to let the bar passes through all field (see speed and field size)
tstop = 1500            # simulation time in milliseconds
cvode_active = 1        # use cvode (1) or fixed time step (0)
cvode_tolerance = 1e-5  # tolerance of CVode
v_init = -60            # initial membrane voltage
# SIMULATION   ################################################################
sampinvl = 0.1
###############################################################################

# Reloading parameters from user-modifiable file
if os.path.exists('./SACnetwork.json'):
    io.load_params_json('SACnetwork.json', globals())

# Converting dend_input_segments to numeric array, in case it was "all"
if dend_input_segments == 'all':
    dend_input_segments = range(0, dendseg)

# Setting up I/O
this_file_path = str(os.path.dirname(os.path.realpath(__file__)))
celldatafilename = this_file_path + '/data/celldata%02g.txt' % dataidx
syndatafilename = this_file_path + '/data/syndata%02g.txt' % dataidx
if not os.path.exists(celldatafilename):
    celldata = topo.create_cell_data(seed=dataidx)
    io.save_cell_data(celldata, celldatafilename)
else:
    celldata = io.read_cell_data(celldatafilename)

# for saving data and plot
today = datetime.date.today()

# Setting up the NEURON environment
h.load_file('stdrun.hoc')  # NEURON'S Libraries
h('proc init() {finitialize()}')  # to avoid that Neuron set initial voltage
if os.getcwd() != this_file_path:  # if same, loaded at importing h
    load_mechanisms(this_file_path)  # load additional mechanisms
h.load_file(str(this_file_path + '/SACtmp.hoc'))  # load SAC template
h.CVode().active(cvode_active)
h.cvode.atol(cvode_tolerance)

# Construct topology using data loaded from files
amac = topo.load_SAC_topology(celldata, ndend, dendseg,
                              diam_min, diam_max)
BPpos = topo.create_bipolar_map(celldata, d_is, is_random=False)
BPsyn, amac = topo.bipolar_SAC_synapses(amac,
                                        BPpos,
                                        ndend,
                                        synapse_type,
                                        dend_input_segments)
if not os.path.exists(syndatafilename):
    synM = topo.create_synapse_matrix(amac, area_thresh, sac_sac_segments)
    io.save_synaptic_data(synM, syndatafilename)
else:
    synM = io.read_synaptic_data(syndatafilename)
gabasyn, amac = topo.load_gabaergic_data(synM, amac, dendseg)
gabasyn = topo.gabaGset(gabasyn, synM, gabaGmax, gabaGmin, k1, k2, th1, th2)


# Steady-state for GABA synapses
def gabaInit(excmin):
    oldtstop = h.tstop
    h.tstop = 5000  # Simulation time
    print "Setting initial glutamatergic synapse..."
    # Set excitatory conductances with minimal tone
    topo.excGset(BPsyn, gmax=excmin, gmin=excmin,
                 synapse_type=synapse_type, tau=BPsyn_tau)
    if is_spatiotemporal:
        topo.apply_spatiotemporal_synaptic_input(BPsyn,
                                                 dend_input_segments,
                                                 BPtau1, BPtau2)
    stim.set_stimulus(BPsyn, stimulus_type, t_es, synapse_type, **stim_param)
    print "Setting gabaergic synapse parameters..."
    topo.gabaGset(gabasyn, synM, gabaGmax, gabaGmin, k1, k2, th1, th2)
    param_log()
    print "Parameters OK. Steady-state simulation started..."
    nrn_init(v_init)
    print "RUN, Neuron...RUN!"
    h.run()
    print "Saving steady-state outputs..."
    initsc1 = [syn.sc1 for syn in gabasyn]
    initsc2 = [syn.sc2 for syn in gabasyn]
    print "Steady-state simulation finished!"
    h.tstop = oldtstop
    return initsc1, initsc2


def init_rec_vector(nrnsec, x=None, var='v'):
    refvar = '_ref_%s' % var  # this is how you get NEURON section's variables
    rec_vec = h.Vector(h.tstop / sampinvl)
    if not x:  # not a section, can be point process for example
        rec_vec.record(getattr(nrnsec, refvar), sampinvl)
    else:
        rec_vec.record(getattr(nrnsec(x), refvar), sampinvl)
    return rec_vec


def param_log():
    print "Working cells are: " + str(amac_rec)

    # PARAMETERS DOCUMENTATION
    dataFiles = {'CELL_GEOMETRY': celldatafilename,
                 'GABA_SYN_INPUT': syndatafilename}
    recording = {'Recorded_amacrine_cells': amac_rec}

    flag = 'Inactive'
    if(h.CVode().active() == 1):
        flag = 'Active'
    neuron_sim_opts = {'tstop': h.tstop,
                       'CVODE': flag,
                       'CVOde_tol': h.CVode().atol(),
                       'Init_V': v_init,
                       'Synaptic model': synapse_type}
    if synapse_type == "alphaCsyn":
        neuron_sim_opts.update({'proximal tau':
                                getattr(h, synapse_type)(0).tau,
                                'distal tau':
                                getattr(h, synapse_type)(1).tau})
    elif synapse_type == "Exp2Syn":
        neuron_sim_opts.update({'proximal tau1':
                                getattr(h, synapse_type)(0).tau1,
                                'distal tau1':
                                getattr(h, synapse_type)(1).tau1,
                                'proximal tau2':
                                getattr(h, synapse_type)(0).tau2,
                                'distal tau2':
                                getattr(h, synapse_type)(1).tau2})
    elif synapse_type == "BPexc":
        neuron_sim_opts.update({'BPtau1': BPtau1,
                                'BPtau2': BPtau2})
    amacrines = {'Segments per dendrite': dendseg,
                 'Min. dendrite diameter': diam_min,
                 'Max. dendrite diameter': diam_max,
                 'Input segments': dend_input_segments}
    bipolar = {'Mean distance': d_is,
               'Max. excitatory conductance': excGmax,
               'Min. excitatory conductance': excGmin}
    gaba_sacs = {'k1': k1,
                 'k2': k2,
                 'th1': th1,
                 'th2': th2,
                 'Max. inhibitory conductance': gabaGmax,
                 'Min. inhibitory conductance': gabaGmin}

    global all_params
    all_params = dict()
    all_params.update(dataFiles)
    all_params.update(neuron_sim_opts)
    all_params.update(amacrines)
    all_params.update(bipolar)
    all_params.update(gaba_sacs)
    all_params.update(recording)


def nrn_init(v0=v_init):
    for a in amac:
        a.setv(v0)
    h.finitialize()


def main(excmax=excGmax, excmin=excGmin, gabaI=-1, main=0, **kwargs):
    if (gabaI != 1 and len(gabaI[0]) == len(gabaI[1]) and
            len(gabaI[0]) == len(gabasyn)):
        print 'init sc1 and sc2'
        for i in range(len(gabasyn)):
            gabasyn[i].sc1init = gabaI[0][i]  # Basal GABA sc1
            gabasyn[i].sc2init = gabaI[1][i]  # Basal GABA sc2
    print "Experiment started!"
    print "Creating excitatory conductances (maxG=%f)..." % excmax

    # Setting glutamatergic synapses
    topo.excGset(BPsyn, gmax=excmax, gmin=excmin,
                 synapse_type=synapse_type, tau=BPsyn_tau)
    if is_spatiotemporal:
        topo.apply_spatiotemporal_synaptic_input(BPsyn,
                                                 dend_input_segments,
                                                 BPtau1, BPtau2)
    print "creating stimuli"
    # Stim properties
    if 'stim_param' in kwargs:
        stim_param = kwargs['stim_param']
    stim.set_stimulus(BPsyn, stimulus_type, t_es, synapse_type, **stim_param)

    global amac_vecs
    global synapse_vecs

    t = h.Vector()
    t.record(h._ref_t, )

    amac_vecs = []
    synapse_vecs = []
    print "Initializing recording vectors..."
    for am in amac_rec:
        v_aux = []
        for xa in x_rec:
            for v in var_amac_rec:
                if sec_rec == 'dend':
                    v1 = init_rec_vector(amac[am].dend[null_dend], xa, v)
                    v2 = init_rec_vector(amac[am].dend[pref_dend], xa, v)
                elif sec_rec == 'soma':
                    v1 = init_rec_vector(amac[am].soma, xa, v)
                    v2 = init_rec_vector(amac[am].soma, .5, v)
                v_aux.append(v1)
                v_aux.append(v2)
        amac_vecs.append(v_aux)
    syn_rec = tl.return_syn_rec(amac_rec, synM, pref_dend, null_dend)
    for syn in syn_rec:
        s_aux = []
        for v in var_syn_rec:
            v1 = init_rec_vector(gabasyn[syn[0]], var=v)
            v2 = init_rec_vector(gabasyn[syn[1]], var=v)
            s_aux.append(v1)
            s_aux.append(v2)
        synapse_vecs.append(s_aux)

    print "Simulation: Started"
    if 'tstop' in kwargs:
        global tstop
        tstop = kwargs['tstop']
    if 'v_init' in kwargs:
        global v_init
        v_init = kwargs['v_init']
    h.tstop = tstop
    nrn_init(v_init)
    h.run()
    param_log()
    print "Simulation: Ended (Yay!)"

    vp = []
    DSv = []
    scp = []
    DSsc = []
    scpa = []
    DSsca = []
    for vvec in amac_vecs:
        v1p, DS1v = tl.DS(t_es, vvec[0].as_numpy(),
                          vvec[1].as_numpy(), sampinvl)
        # Max diff voltage preferred dendrite to its base
        vp.append(v1p)
        DSv.append(DS1v)  # DSI de voltaje

    for scvec in synapse_vecs:
        # Note that DSI is computer over first var_syn_rec, by default sc2
        sc1p, DS1sc = tl.DS(t_es, scvec[0].as_numpy(),
                            scvec[1].as_numpy(), sampinvl)
        sc1pa, DS1sca = tl.DS(t_es, scvec[0].as_numpy(),
                              scvec[1].as_numpy(), sampinvl, area=1)
        scp.append(sc1p)  # Dif max sc2 preferred dendrite
        # Max area diff preferred dendrite to its base
        scpa.append(sc1pa)
        DSsc.append(DS1sc)  # DSI sc2
        # Max area diff null and preferred dendrites
        DSsca.append(DS1sca)
    if stimulus_type in ('bar', 'bar_with_circular_mask'):
        result = np.hstack((stim_param['bar_width'],
                            stim_param['bar_speed'],
                            np.hstack([v for v in (vp +
                                                   DSv +
                                                   scp +
                                                   DSsc +
                                                   scpa +
                                                   DSsca)])))
    elif stimulus_type == 'annulus':
        result = np.hstack((stim_param['inner_diam'],
                            stim_param['outer_diam'],
                            np.hstack([v for v in (vp +
                                                   DSv +
                                                   scp +
                                                   DSsc +
                                                   scpa +
                                                   DSsca)])))
    else:
        print "Wrong stimulus type: %s" % stimulus_type
    if main == 0:
        return result
    else:
        return result, amac_vecs, synapse_vecs

def getGlobals():
    return globals();     