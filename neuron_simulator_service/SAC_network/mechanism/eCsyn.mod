:
:
NEURON	{
  POINT_PROCESS expCSyn
  RANGE minG, maxG, dur, onset, default_dur
  RANGE e, tau, g, A
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
    default_dur = 5    (ms)
	dur        = 5     (ms)  : duration of stimulus
    onset      = 5      (ms) : onset of stimulus
	e          = 0      (mV) : reversal potential
    tau        = 10      (ms)  : time constant (delay) of synaptic response
    amp        = 1 : Scaling factor. DON'T TOUCH unless with Vector.play()
}

ASSIGNED {
    g       (uS)
    v           (mV)
    i           (nA)
    A
}

INITIAL {
    a=0
}

STATE {
    a
}

BREAKPOINT {
	at_time(onset)
	at_time(onset+dur)
    Astate()
    SOLVE states METHOD cnexp
    g = minG + (maxG - minG)* a
    i = g * ( v - e )
}

DERIVATIVE states {
    a' = (A - a)/tau

}

PROCEDURE Astate() {
	if (t < onset + dur && t >= onset) {
		A = amp
	}else{
		A = 0
	}
}