: 
: 
NEURON	{ 
  POINT_PROCESS ContSynapse
  RANGE minG, maxG, dur, onset
  RANGE e, tau
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
	dur        = 5     (ms)  : duration of stimulus
    onset      = 5      (ms) : onset of stimulus
	e          = 0      (mV) : reversal potential
:	noise		= 0 <0,1>	 : amount of randomness (0.0 - 1.0)
	gmax       = 0.1   (uS)
}

ASSIGNED {
    g       (uS)
    v           (mV)
    i           (nA)
}

INITIAL {
    g=minG
}

BREAKPOINT {
:    at_time(onset)
:    at_time(onset+dur)
    calcG()   
    i = g*(v-e)
}
	
PROCEDURE calcG() {
    if (t < onset + dur && t >= onset) {
        g = minG + (maxG - minG)*sin(3.14159*( t -onset)/dur)
	} else {
        g = minG
    }
}

