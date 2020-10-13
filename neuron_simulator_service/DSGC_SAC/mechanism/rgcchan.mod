TITLE RGC channels

: 01/2018
: Leo Medina
: Based on Fohlmeister et al (2010), J Neurophys
: "Mechanisms and distribution of ion channels in retinal ganglion cells"

NEURON {
    SUFFIX rgcchan
    USEION na READ ena WRITE ina
    USEION k READ ek WRITE ik
    USEION ca READ eca WRITE ica
    RANGE gnabar, gkbar, gcabar
    RANGE m_inf, h_inf, n_inf, c_inf
    RANGE tau_m, tau_h, tau_n, tau_c
}


UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
}

PARAMETER {

    : Defaults for axon
    gnabar  = 0.124 (mho/cm2)
    gkbar   = 0.05  (mho/cm2)
    gcabar  = 0.0   (mho/cm2)
    ena     = 60.0  (mV)
    ek      = -100.0 (mV)
    eca     = 90.0 (mV)

    : At 35C
    amA = 2.725
    amB = 35
    amC = -10
    bmA = 90.83
    bmB = 60
    bmC = -20

    ahA = 1.817
    ahB = 52
    ahC = -20
    bhA = 27.25
    bhB = 22
    bhC = -10

    anA = 0.09575
    anB = 37
    anC = -10
    bnA = 1.915
    bnB = 47
    bnC = -80

    acA = 1.362
    acB = 13
    acC = -10
    bcA = 45.41
    bcB = 38
    bcC = -18
}

STATE {
    m h n c
}

ASSIGNED {
    v     (mV)
    ina   (mA/cm2)
    ik    (mA/cm2)
    ica   (mA/cm2)
    m_inf
    h_inf
    n_inf
    c_inf
    tau_m
    tau_h
    tau_n
    tau_c
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    ina = gnabar * m*m*m * h * (v - ena)
    ik  = gkbar * n*n*n*n * (v - ek)
    ica = gcabar * c*c*c * (v - eca)
}

DERIVATIVE states {   : exact Hodgkin-Huxley equations
    evaluate_fct(v)
    m' = (m_inf - m) / tau_m
    h' = (h_inf - h) / tau_h
    n' = (n_inf - n) / tau_n
    c' = (c_inf - c) / tau_c
}

UNITSOFF

INITIAL {

    evaluate_fct(v)
    m = m_inf
    h = h_inf
    n = n_inf
    c = c_inf
}

PROCEDURE evaluate_fct(v(mV)) { LOCAL a, b

    a = vtrap1(v, amA, amB, amC)
    b = vtrap3(v, bmA, bmB, bmC)
    tau_m = 1 / (a + b)
    m_inf = a / (a + b)

    a = vtrap3(v, ahA, ahB, ahC)
    b = vtrap2(v, bhA, bhB, bhC)
    tau_h = 1 / (a + b)
    h_inf = a / (a + b)

    a = vtrap1(v, anA, anB, anC)
    b = vtrap3(v, bnA, bnB, bnC)
    tau_n = 1 / (a + b)
    n_inf = a / (a + b)

    a = vtrap1(v, acA, acB, acC)
    b = vtrap3(v, bcA, bcB, bcC)
    tau_c = 1 / (a + b)
    c_inf = a / (a + b)
}

FUNCTION vtrap1(x, A, B, C) {
    if (fabs((x + B) / C) < 1e-6) {
        vtrap1 = A * C
    }else{
        vtrap1 = (A * (x + B)) / (1 - Exp((x + B) / C))
    }
}

FUNCTION vtrap2(x, A, B, C) {
    if (x < -50) {
        vtrap2 = 0
    }else{
        vtrap2 = A / (1 + Exp((x + B) / C))
    }
}

FUNCTION vtrap3(x, A, B, C) {
    vtrap3 = A * Exp((x + B) / C)
}

FUNCTION Exp(x) {
    if (x < -100) {
        Exp = 0
    }else{
        Exp = exp(x)
    }
}

UNITSON