import numpy as np
import json


def read_cell_data(celldatafilename):
    """Read cell data from file"""
    celldata = np.loadtxt(celldatafilename, skiprows=1)
    return celldata


def save_cell_data(celldata, celldatafilename):
    """Save synaptic data to file"""
    with open(celldatafilename, "a") as text:
        np.savetxt(text, np.array(celldata.shape)[None], "%d")
        np.savetxt(text, celldata, "%12.6g")


def read_synaptic_data(syndatafilename):
    """Read synaptic data from file"""
    synM = np.loadtxt(syndatafilename, skiprows=1)
    return synM


def save_synaptic_data(synM, syndatafilename):
    """Save synaptic data to file"""
    with open(syndatafilename, "a") as text:
        np.savetxt(text, np.array(synM.shape)[None], "%d")
        np.savetxt(text, synM, "%12.8g")


def load_params_json(jsonfile, global_param_dict):

    with open(jsonfile, 'r') as fp:
        file_param_dict = json.load(fp)

    for key, value in file_param_dict.iteritems():
        if key not in global_param_dict:
            print 'Warning! Parameter %s in json file is unknown' % key

    global_param_dict.update(file_param_dict)
    return file_param_dict


def save_gabaInit_file(ginit, SACnetwork_params, jsonfile):
    the_dict = {'initsc1': ginit[0],
                'initsc2': ginit[1]}
    # Include network params for file identification by user outside
    the_dict.update(SACnetwork_params)
    with open(jsonfile, 'w') as fp:
        json.dump(the_dict, fp)


def load_gabaInit_file(jsonfile):
    with open(jsonfile, 'r') as fp:
        file_param_dict = json.load(fp)
    return file_param_dict['initsc1'], file_param_dict['initsc2']


def save_params_json(jsonfile, param_dict):

    with open(jsonfile, 'w') as fp:
        json.dump(param_dict, fp)
