: 
: 
NEURON	{ 
  POINT_PROCESS GABAsyn
  POINTER vpre
  RANGE minG, maxG, e, k1, k2, th1, th2, sc1init, sc2init
  NONSPECIFIC_CURRENT i
  THREADSAFE
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
    minG    = 0.000014 (uS)    : min (basal) conductance
    maxG    = 0.00042 (uS)  : max conductance
    e       = -60      (mV) : reversal potential
    th1     = -50       (mV)
    th2     = 0.3
    alpha   = 0.08 (/ms)
    beta    = 0.006  (/ms)
    k1      = 0.2   (mV)  
    k2      = 0.02
    sc1init = 0
    sc2init = 0
}

ASSIGNED {
    g       (uS)
    v           (mV)
    vpre        (mV)
    i           (nA)
    H1
    H2
}

INITIAL {
    if (sc1init==0) {
        H1 = 1/(1+exp(-(vpre-th1)/k1))
        sc1=alpha*H1/(alpha*H1+beta)
    }
    else {
    sc1=sc1init
    }
    if (sc2init==0) {
        H2 = (sc1^(1/k2))/((th2^(1/k2))+(sc1^(1/k2)))
        sc2=alpha*H2/(alpha*H2+beta)
    }
    else {
    sc2=sc2init
    }

    g=minG + (maxG-minG)*sc2
}

STATE {
    sc1
    sc2    
}
BREAKPOINT {
    SOLVE states METHOD cnexp   
    g = minG + (maxG-minG)*sc2
    i = g * (v - e)
}
	
DERIVATIVE states{
    H1 = 1/(1+exp(-(vpre-th1)/k1))
    H2 = (sc1^(1/k2))/((th2^(1/k2))+(sc1^(1/k2)))
    
    sc1' = alpha*(1-sc1)*H1 - beta*sc1
    sc2' = alpha*(1-sc2)*H2 - beta*sc2    
}

