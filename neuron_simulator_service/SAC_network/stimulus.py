from __future__ import division
import numpy as np


# Set bar stimuli speed
def update_bar_speed(BPsyn, delay, width, speed, d_init,
                     synapse_type="alphaCSyn", angle=0):
    print "Updating bar speed to: %f mm/s" % speed
    angrad = angle * np.pi / 180.0
    angcos = np.cos(angrad)
    angsin = np.sin(angrad)

    for BPi in BPsyn:
        # Note that initial bar position, d_init, should be as far as to
        # ensure all BP are activated
        # (xprime, yprime): rotated and translated axes centered on the bar
        # xprime: axis of bar, yprime: normal to bar
        # xprime = BPi[1] * angsin - BPi[2] * angcos
        yprime = BPi[1] * angcos + BPi[2] * angsin + d_init
        synapse_onset = delay + yprime / speed
        if ((speed > 0 and yprime < (0 - width)) or
           (speed < 0 and yprime > 0)):
            # Bar won't pass over BP location (yprime)
            deactivate_BP_synapse(BPi, synapse_type, synapse_onset)
            continue
        duration = None
        if synapse_type == "BPexc":
            duration = abs(width / speed)
        activate_BP_synapse(BPi, synapse_type, synapse_onset, duration)
    return BPsyn


def set_stimulus(BPsyn, stimulus_type, delay, synapse_type, **kwargs):
    if stimulus_type == "bar":
        width = kwargs['bar_width']
        speed = kwargs['bar_speed']
        x_init = kwargs['bar_x_init']
        if 'bar_angle' in kwargs:
            update_bar_speed(BPsyn, delay, width, speed, x_init, synapse_type,
                             kwargs['bar_angle'])
        else:
            update_bar_speed(BPsyn, delay, width, speed, x_init, synapse_type)
    elif stimulus_type == "annulus":
        center = kwargs['center']
        ri = kwargs['inner_diam']
        ro = kwargs['outer_diam']
        dur = kwargs['duration']
        print "Setting up annulus stimulus with delay: %1.1f (ms)" % delay
        for BPi in BPsyn:
            if in_annulus((BPi[1], BPi[2]), center, ri, ro):
                activate_BP_synapse(BPi, synapse_type, delay, dur)
    elif stimulus_type == "grating":
        width = kwargs['bar_width']
        speed = kwargs['bar_speed']
        x_init = kwargs['bar_x_init']
        x_freq = kwargs['spatial_freq']
        N_bars = kwargs['N_bars']
        dur = width / speed
        period = x_freq / speed
        for BPi in BPsyn:
            if BPi[1] < (x_init - width):  # Grating wont pass over BP location
                continue
            synapse_onset = delay + (BPi[1] - x_init) / speed
            activate_BP_synapse(BPi, synapse_type, synapse_onset, dur, period,
                                N_bars)
    elif stimulus_type == "bar_with_circular_mask":
        width = kwargs['bar_width']
        speed = kwargs['bar_speed']
        x_init = kwargs['bar_x_init']
        mask_center = kwargs['mask_center']
        mask_diam = kwargs['mask_diam']
        dur = width / speed
        for BPi in BPsyn:
            if BPi[1] < (x_init - width) or not in_annulus((BPi[1], BPi[2]),
               mask_center, 0, mask_diam / 2):
                continue
            synapse_onset = delay + (BPi[1] - x_init) / speed
            activate_BP_synapse(BPi, synapse_type, synapse_onset, dur)
    return BPsyn


def in_annulus(point, center, inner_diam, outer_diam):
    dist = np.linalg.norm(np.array(point) - np.array(center))
    return dist >= inner_diam and dist <= outer_diam


def activate_BP_synapse(BPsynapse, synapse_type, synapse_onset, dur=None,
                        period=0, n_events=1):
    if synapse_type in ("alphaCSyn", "expCSyn"):
        BPsynapse[0].onset = synapse_onset
        BPsynapse[0].dur = BPsynapse[0].default_dur
        if dur is not None:
            BPsynapse[0].dur = dur
    elif synapse_type in ("Exp2Syn", "BPexc"):
        BPsynapse[-2].number = n_events
        BPsynapse[-2].interval = period
        BPsynapse[-2].start = synapse_onset
        BPsynapse[-2].noise = 0  # Deafult should be 0 anyway
        if synapse_type == "BPexc":
            BPsynapse[0].dur = dur


def deactivate_BP_synapse(BPsynapse, synapse_type, synapse_onset):
    if synapse_type in ("alphaCSyn", "expCSyn"):
        BPsynapse[0].onset = synapse_onset
        BPsynapse[0].dur = 0
    elif synapse_type in ("Exp2Syn", "BPexc"):
        BPsynapse[-2].number = 0
        BPsynapse[-2].interval = 0
        BPsynapse[-2].start = synapse_onset
        BPsynapse[-2].noise = 0  # Deafult should be 0 anyway
        if synapse_type == "BPexc":
            BPsynapse[0].dur = 0


def insert_voltage_clamp(nrnobj, nrnsec, xsec, voltage_amp, dur):
    vclamp = nrnobj.SEClamp(xsec, sec=nrnsec)
    vclamp.amp1 = voltage_amp
    vclamp.dur1 = dur
    return vclamp
