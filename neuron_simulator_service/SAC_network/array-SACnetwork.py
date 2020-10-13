"""
Created on Tue May 30, 2017

@author: Leo Medina
"""
import SACnetwork
import numpy as np
import time
import datetime
import os
import iodef as io
import sys

def scoped(param):
    # Parameters
    ###############################################################################
    G_MIN_EXP = -6
    G_MAX_EXP = -3
    G_NUMBER = 20
    VELOC_MIN_EXP = -1
    VELOC_MAX_EXP = 2
    VELOC_NUMBER = 20
    PARAM_NUMBER = param
    ###############################################################################

    # Recording vectors
    timevec = SACnetwork.h.Vector()
    timevec.from_python(np.arange(0, SACnetwork.tstop, SACnetwork.sampinvl))
    timerec = SACnetwork.h.Vector()
    timerec.record(SACnetwork.h._ref_t, timevec)

    if os.path.exists('./array-SACnetwork.json'):
        io.load_params_json('./array-SACnetwork.json', globals())
    if os.path.exists('./gabaInit.json'):
        print "Loading GABA initial parameters from file..."
        sc1i, sc2i = io.load_gabaInit_file('./gabaInit.json')
    else:
        sc1i, sc2i = SACnetwork.gabaInit(SACnetwork.excGmin)

    gmax = np.logspace(G_MIN_EXP, G_MAX_EXP, G_NUMBER)
    stimuliSpeed = np.logspace(VELOC_MIN_EXP, VELOC_MAX_EXP, VELOC_NUMBER)
    synapse_type = SACnetwork.synapse_type  # Note this param is in SACnetwork.py
    params = [(g, v) for g in gmax for v in stimuliSpeed]

    start_time = time.time()
    today = datetime.date.today()

    print "Simulation using " + synapse_type
    print "Starting simulation: "

    simPath = "./results/%s/" % today

    if not os.path.exists(simPath):  # only process 0 attempts to create folder
        os.makedirs(simPath)

    numv = len(SACnetwork.amac_rec)
    numsc = len(SACnetwork.amac_rec)
    head_entries = ['v%dp' % n for n in range(numv)] + \
        ['DSv%d' % n for n in range(numv)] + \
        ['sc%dp' % n for n in range(numsc)] +\
        ['DSsc%d' % n for n in range(numsc)] +\
        ['sc%dpa' % n for n in range(numsc)] +\
        ['DSsca%d' % n for n in range(numsc)]

    head = 'speed,gmax,width,speed1,' + ','.join(head_entries)

    grid = {'Initial speed': stimuliSpeed[0],
            'Final Speed': stimuliSpeed[-1],
            'Speed points': len(stimuliSpeed),
            'Initial conductance': gmax[0],
            'Final conductance': gmax[-1],
            'Conductance points': len(gmax)}

    if not isinstance(PARAM_NUMBER, list):
        PARAM_NUMBER = [PARAM_NUMBER]

    res = []
    for param_num in PARAM_NUMBER:
        g, sp = params[int(param_num)]
        print "Running sim with speed %f and max conductance %f" % (sp, g)
        SACnetwork.stim_param['bar_speed'] = sp
        # Assuming a field of about 1 mm, simulation must be long enough for bar to
        # cover the entire field. sp in mm/s, multiply by 1000 to convert to ms
        t_total = SACnetwork.t_es + (1.0 +
                                    SACnetwork.stim_param['bar_width'] /
                                    1000.0) / sp * 1000.0
        if t_total < 1500:
            t_total = 1500  # Sim no shorter than 1.5 s, see calculation of DSI
        SACnetwork.tstop = t_total
        res_i = SACnetwork.main(gabaI=(sc1i, sc2i),
                                excmax=g,
                                stim_param=SACnetwork.stim_param)
        res_i = np.hstack([sp, g, np.hstack(res_i)])
        res.append(res_i)
        print "Time elapsed: ", time.time() - start_time, "s"
        np.savetxt(simPath +
                synapse_type +
                '_%s_%s_%s_gmax_data%s_heat-grande_%s_array%s.txt' %
                (SACnetwork.amac_rec[0], SACnetwork.amac_rec[1],
                    SACnetwork.amac_rec[2], SACnetwork.dataidx,
                    SACnetwork.today,
                    param_num),
                np.array(res_i[None]),
                fmt='%6g', delimiter=',', header=head)
        param_set = {'Speed': sp,
                    'Conductance': g}
        # Parameters
        params_dict = dict()
        params_dict.update(param_set)
        params_dict.update(grid)
        params_dict.update(SACnetwork.all_params)
        io.save_params_json(simPath +
                            synapse_type +
                            '_simulation_parameters_%s_%s.json' %
                            (SACnetwork.today, param_num), params_dict)

    if len(PARAM_NUMBER) > 1:
        np.savetxt(simPath +
                synapse_type +
                '_%s_%s_%s_gmax_data%s_heat-grande_%s_all.txt' %
                (SACnetwork.amac_rec[0], SACnetwork.amac_rec[1],
                    SACnetwork.amac_rec[2], SACnetwork.dataidx,
                    SACnetwork.today),
                np.array(res),
                fmt='%6g', delimiter=',', header=head)

    #added
    listResult = []
    for element in res:
        listResult.append(element.tolist())

    #tricky
    listResult = listResult[0]    

    resultsDict = {}

    staticEntries = ['speed', 'gmax', 'width', 'speed1']
    dynamicEntries = ['vp', 'DSvd', 'scp', 'DSsc', 'scpa', 'DSsca']

    i = 0
    j = 0
    resultsPerCell = numv

    print len(listResult)
    while i < len(staticEntries):
        resultsDict[staticEntries[i]] = listResult[i]
        i += 1

    while j < len(dynamicEntries):
        resultsDict[dynamicEntries[j]] = listResult[i:i+numv]
        j +=1
        i += 1

   
    parsedSynapseVecs = []
    parsedAmacVecs = []

    for vector in SACnetwork.synapse_vecs:
        parsedSynapseVecs.append(list(vector[0]))
        parsedSynapseVecs.append(list(vector[1]))

    for vector in SACnetwork.amac_vecs:
        parsedAmacVecs.append(list(vector[0]))
        parsedAmacVecs.append(list(vector[1]))    

    resultsDict["resultsPerCell"] = resultsPerCell 
    resultsDict["simulationTime"] = str(time.time() - start_time)
    resultsDict["cells"] = map(str, SACnetwork.amac_rec)
    resultsDict["timeRec"] = list(timerec)  
    resultsDict["amacVecs"] = parsedAmacVecs 
    resultsDict["synapseVecs"] = parsedSynapseVecs

    return resultsDict

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   scoped(0)               
