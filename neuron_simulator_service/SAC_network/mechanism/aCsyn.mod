:
:
NEURON	{
  POINT_PROCESS alphaCSyn
  RANGE minG, maxG, dur, onset, default_dur
  RANGE e, tau, g
  NONSPECIFIC_CURRENT i
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
    minG    = 0.00001 (uS)    : min (basal) rate, Hz
    maxG    = 0.001 (uS)  : max rate, Hz
	default_dur= 100    (ms)
    dur        = 100    (ms) : duration of synaptic release
    onset      = 5      (ms) : delay
	e          = 0      (mV) : reversal potential
    tau        = 2      (ms)  : time constant (delay) of synaptic response
    amp        = 1 (1/ms) : Scaling factor. DON'T TOUCH unless with Vector.play()
}

ASSIGNED {
    g       (uS)
    v           (mV)
    i           (nA)
    A           (/ms)
}

INITIAL {
    a2=0
    a1=0
}

STATE {
    a1
    a2  (1/ms)
}

BREAKPOINT {
    Astate()
    SOLVE states METHOD cnexp
    g = minG + (maxG - minG)* (a1 *1(ms)/tau)
    i = g * ( v - e )
}

DERIVATIVE states {
:    LOCAL dz
:    dz = A/tau - 2*a2/tau - a1/(tau^2)
    a2' = A/tau - 2*a2/tau - a1/(tau*tau)
    a1' = a2
}

PROCEDURE Astate() {
	if (t < onset + dur && t >= onset) {
		A = amp
	}else{
		A = 0
	}
}