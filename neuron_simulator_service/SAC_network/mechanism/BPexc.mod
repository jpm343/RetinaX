COMMENT
Bipolar-SAC synapse based on measurements of Borghuis et al (2013).
Sustained synapse type. See Figure 3C for a 0.5 sec stimulus.
Assuming g decays to about half the maximal g in 0.5 sec. Note that
in Figure 8C, we can find a IPL depth where the response will satify this.

ENDCOMMENT

NEURON {
    POINT_PROCESS BPexc
    RANGE minG, maxG, dur
    RANGE e, tau1, tau2, g, active
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

PARAMETER {
    minG  = 0.00001 (uS) : min conductance
    maxG  = 0.001   (uS) : max conductance
    dur   = 100     (ms) : duration of synaptic release
    e     = 0       (mV) : reversal potential
    tau1  = 20       (ms) : time constant of synaptic response (rise)
    tau2  = 900       (ms) : time constant of synaptic response (decay)
}

ASSIGNED {
    g (uS)
    v (mV)
    i (nA)
    active (1)
}

STATE {
    A (1)
    B (1)
    :active (1)
}

INITIAL {
    A = 0
    B = 0
    active = 0
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    g = minG + active*((maxG-minG)*(B - A))
    i = g * (v - e)
}

DERIVATIVE states {
    A' = -A/tau1
    B' = -B/tau2
}

NET_RECEIVE(weight (uS)) {
    if(flag == 0 && dur > 0){
        active = 1
        A = 1
        B = 1
        net_send(dur, 1) : self-event to stop activation after "dur"; see "else"

    }else{
        active = 0
    }

}