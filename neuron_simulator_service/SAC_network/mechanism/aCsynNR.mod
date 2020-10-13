COMMENT
Alpha Continuous Synapse activated with events from
NetCon objects, i.e., it has the NET_RECEIVE block

ENDCOMMENT

NEURON {
    POINT_PROCESS alphaCSynNR
    RANGE minG, maxG, dur, onset
    RANGE e, tau, g
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
    onset = 5       (ms) : delay
    e     = 0       (mV) : reversal potential
    tau   = 2       (ms) : time constant of synaptic response
    amp   = 1       (1/ms) : Scaling factor
}

ASSIGNED {
    g (uS)
    v (mV)
    i (nA)
    A (/ms)
}

STATE {
    a1
    a2  (1/ms)
}

INITIAL {
    a2 = 0
    a1 = 0
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    g = minG + (maxG - minG)* (a1 *1(ms)/tau)
    i = g * (v - e)
}

DERIVATIVE states {
    a2' = A/tau - 2*a2/tau - a1/(tau*tau)
    a1' = a2
}

NET_RECEIVE(weight (uS)) {
    if(flag == 0){
        A = A + amp
        net_send(dur, 1) : self-event to stop activation after "dur"; see "else"
    }else{
        A = 0
    }

}