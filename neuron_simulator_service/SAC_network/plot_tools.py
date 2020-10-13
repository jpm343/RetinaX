#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 13:51:06 2017

@author: leo
"""
import numpy as np
import pandas as pd
import os
import matplotlib.cm as cmx
import matplotlib.pyplot as plt
import json
import glob


def heat_map(datafile, outfolder,
             thevar="DSsc", varx="# speed", vary="gmax",
             get_average=False,
             sac_number=None):

    data = pd.read_csv(datafile)
    if '# vel' in data and varx == "# speed":
        varx = 'vel'
    x = data[varx].values
    y = data[vary].values
    ux = np.unique(x)
    uy = np.unique(y)
    X, Y = np.meshgrid(ux, uy)

    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    if sac_number is None:
        if thevar == "dsi":
            sac_number = ("-1",)
        else:
            fileparts = datafile.split('_')
            sac_number = [f for f in fileparts if f.isdigit()]
    si = 0
    Z_avg = []
    for sac in sac_number:
        datakey = thevar
        if thevar != 'dsi':
            datakey = thevar + str(si)
        z = np.array(data[datakey])
        z = np.ma.masked_invalid(z.astype(float))
        Z = np.empty(X.shape)
        # The following is to fill matrix with NaN's in case not all
        # simulations are available
        for i in range(0, len(ux)):
            for j in range(0, len(uy)):
                zaux = z[(x == X[i, j]) & (y == Y[i, j])]
                if zaux.size > 0:
                    Z[i, j] = zaux
                else:
                    Z[i, j] = np.nan
        if get_average:
            Z_avg.append(Z)
        fig, ax = plt.subplots()
        plt.set_cmap('jet')
        plt.title('SAC number: ' + str(sac))
        plt.set_cmap('jet')
        cax = ax.pcolormesh(X, Y, Z, vmin=0, vmax=1, snap=True)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_ylabel('$Stim\/\ intensity,\/\ g_{max} \/\ (\mu S)$',
                      fontsize=15)
        ax.set_ylim(min(y), max(y))
        ax.set_xlim(min(x), max(x))
        ax.set_xlabel('$Speed\/\ (mm/s)$', fontsize=15)
        cbar = fig.colorbar(cax, ticks=[0, 0.5, 1])
        cbar.set_label('$DSI$', fontsize=15)
        plt.tight_layout()
        plt.savefig(os.path.join(outfolder,
                                 'heatmap-' + thevar + str(sac) + '.png'),
                    dpi=300,
                    transparent=True)
        plt.close()
        si += 1
        plt.close(fig)
    if get_average:
        Z_avg = np.mean(Z_avg, axis=0)
        fig, ax = plt.subplots()
        plt.set_cmap('jet')
        plt.title('Average of SACs')
        plt.set_cmap('jet')
        cax = ax.pcolormesh(X, Y, Z, vmin=0, vmax=1, snap=True)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_ylabel('$Stim\/\ intensity,\/\ g_{max} \/\ (\mu S)$',
                      fontsize=15)
        ax.set_ylim(min(y), max(y))
        ax.set_xlim(min(x), max(x))
        ax.set_xlabel('$Speed\/\ (mm/s)$', fontsize=15)
        cbar = fig.colorbar(cax, ticks=[0, 0.5, 1])
        cbar.set_label('$DSI$', fontsize=15)
        plt.tight_layout()
        plt.savefig(os.path.join(outfolder,
                                 'heatmap-' + thevar + '_average.png'),
                    dpi=300,
                    transparent=True)
        plt.close()
        plt.close(fig)


def print_param(file):
    if not os.path.exists(file):
        print "No parameters file. Default parameters were used..."
        return
    with open(file, "r") as fp:
        param = json.load(fp)
    for key in param:
        print key + " = " + str(param[key])


def move_figs(src, dest):
    flist = glob.glob(src + '*.png')
    if not os.path.exists(dest):
        os.mkdir(dest)
    from shutil import copyfile
    for f in flist:
        copyfile(f, dest)


def gather_results(folder, ext="txt", selection=None):
    filelist = glob.glob(os.path.join(folder, "*" + ext))
    s = list()
    for f in filelist:
        r = f.replace(ext, '').split('_')[-1]  # remove ext
        s.append(int(''.join(x for x in r if x.isdigit())))
    notfound = [i for i in range(max(s) + 1) if i not in s]
    found = [i for i in range(max(s) + 1) if i not in notfound]
    if notfound:
        print "Warning! Not found: ", notfound
    rootstr = f.split('_array')[0] + '.txt'  # to be used as output filename
    if selection is not None:
        found = found and selection
    filelist = [filelist[s.index(i)] for i in found]  # sorted
    df = pd.DataFrame()
    for f in filelist:
        df = df.append(pd.read_csv(f), ignore_index=True)
    df.to_csv(rootstr)
    return rootstr


def gather_results_special(folder,
                           ext="txt",
                           ext_sp="_dsi.txt",
                           col1="# speed",
                           col2="gmax"):
    filelist = glob.glob(os.path.join(folder, "*" + ext))
    filelist_sp = glob.glob(os.path.join(folder, "*" + ext_sp))
    filelist = [x for x in filelist if x not in filelist_sp]
    s = list()
    s_sp = list()
    for f in filelist:
        r = f.replace(ext, '').split('_')[-1]
        s.append(int(''.join(x for x in r if x.isdigit())))
    for f in filelist_sp:
        r = f.replace(ext_sp, '').split('_')[-1]  # remove ext
        s_sp.append(int(''.join(x for x in r if x.isdigit())))
    notfound = [i for i in range(max(s) + 1) if i not in s]
    if notfound:
        print "Warning! Not found: ", notfound
    if len(filelist) != len(filelist_sp):
        print "Warning! Lists of different length"
    rootstr = f.split('_array')[0] + '.txt'  # to be used as output filename
    filelist = [filelist[s.index(i)] for i in range(len(s))]  # sorted
    filelist_sp = [filelist_sp[s_sp.index(i)] for i in range(len(s_sp))]
    df = pd.DataFrame(columns=[col1, col2, "dsi"])
    for (f, f_sp) in zip(filelist, filelist_sp):
        rf = pd.read_csv(f)
        df = df.append({col1: rf[col1][0],
                        col2: rf[col2][0],
                        "dsi": np.loadtxt(f_sp)}, ignore_index=True)
    df.to_csv(rootstr)
    return rootstr


def bipolar_SAC_map(SACntw,
                    outfolder,
                    DSGC=None,
                    BPpos=None,
                    SACpos=None,
                    whichSAC=None):
    celldata = SACntw.celldata
    labels = ['SAC {0}'.format(j) for j in range(len(celldata))]
    BPcoord = np.array(SACntw.BPpos)

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_position([0.1, 0.1, 0.7, 0.8])
    colrs = cmx.gist_rainbow(np.linspace(0, 1, len(celldata)))
    for i in range(len(celldata)):
        ax.scatter(celldata[i, 0], celldata[i, 1], s=celldata[i, 2],
                   c=colrs[i], alpha=0.8, label=labels[i])

    ax.legend(scatterpoints=1,
              loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=False, shadow=False, ncol=10, fontsize=8)
    ax.scatter(BPcoord[:, 0], BPcoord[:, 1], s=1, color='grey')
    ax.axis('scaled')
    plt.xlabel('x coordinate ($\mu$m)')
    plt.ylabel('y coordinate ($\mu$m)')
    if DSGC is not None:
        for sec in DSGC.all:
            n3d = SACntw.h.n3d(sec=sec)
            xtuple = (SACntw.h.x3d(0, sec=sec),
                      SACntw.h.x3d(n3d - 1, sec=sec))
            ytuple = (SACntw.h.y3d(0, sec=sec),
                      SACntw.h.y3d(n3d - 1, sec=sec))
            plt.plot(xtuple, ytuple, color='black')
        if BPpos is not None:
            ax.scatter(BPpos[:, 0], BPpos[:, 1], s=5, color='green')
        if SACpos is not None:
            ax.scatter(SACpos[:, 0], SACpos[:, 1], s=10, color='red')
        if whichSAC is not None:
            for ws in whichSAC:
                ax.scatter(celldata[ws, 0], celldata[ws, 1],
                           marker="x", c="red", alpha=1,
                           label=labels[ws])
    import ntpath
    fn = (ntpath.basename(SACntw.celldatafilename).replace('.txt', '_') +
          ntpath.basename(SACntw.syndatafilename).replace('.txt', '_') +
          'network.png')
    plt.savefig(os.path.join(outfolder, fn), dpi=300, transparent=True)


def plot_vec_recorded(SACntw, Vvecs, outfolder='', vec_type='v', dsi='',
                      **kargs):

    if vec_type == 'v':
        ylim = (-70, 0)
        ylabel = 'Voltage (mV)'
    elif vec_type == 'sc':
        ylim = (0, 1)
        ylabel = '$\mathrm{G_{GABA}/G_{max}}$'

    amac_rec = SACntw.amac_rec
    colrs = cmx.gist_rainbow(np.linspace(0, 1, len(SACntw.celldata)))

    # plt.clf()
    # plt.subplots(figsize=(20, 20))

    label_null = ['SAC %g null' % (i) for i in amac_rec]
    label_pref = ['SAC %g preferred' % (i) for i in amac_rec]
    if 'subplot' in kargs.keys():
        plt.subplot(kargs['subplot'])
    else:
        plt.figure()
        plt.subplot(111)

    if dsi is not '':
        title = '\n'.join([('SAC%d DSI= %.2f' % (k, n))
                           for n, k in zip(dsi, amac_rec)])
        plt.title(title)
    for i in range(0, len(amac_rec)):
        for j in range(0, len(SACntw.x_rec)):
            vvec = Vvecs[i][2 * j + 1].as_numpy()[0:int(SACntw.h.tstop /
                                                        SACntw.sampinvl)]
            plt.plot(np.arange(0, SACntw.h.tstop, SACntw.sampinvl), vvec,
                     color=colrs[amac_rec[i]] * (j + 1) / len(SACntw.x_rec),
                     ls='--', lw=2, label=label_null[i])
            vvec = Vvecs[i][2 * j].as_numpy()[0:int(SACntw.h.tstop /
                                                    SACntw.sampinvl)]
            plt.plot(np.arange(0, SACntw.h.tstop, SACntw.sampinvl),
                     vvec, color=colrs[amac_rec[i]] * (j + 1) / len(SACntw.x_rec),
                     ls='-', lw=2, label=label_pref[i])
    plt.ylim(ylim)
    plt.ylabel(ylabel, fontsize=16)
    plt.xlim(50, SACntw.h.tstop)
    plt.xlabel('Time (ms)')
    plt.legend(prop={'size': 12}, loc='best',
               fancybox=False, ncol=len(Vvecs[0]),
               frameon=False, facecolor='inherit')

    if outfolder != '':  # Save to file if outfolder not empty
        name = ','.join(str(n) for n in amac_rec)

        namefig = os.path.join(outfolder,
                               (SACntw.synapse_type +
                                "_%s_%s_%s.png"))

        plt.savefig(namefig % (str(SACntw.today),
                               name, vec_type), dpi=300, transparent=True)


def SAC_map(SACntw, outfolder, DSGC=None):
    celldata = SACntw.celldata
    amac_rec = SACntw.amac_rec
    labels = ['SAC {0}'.format(j + 1) for j in range(len(celldata))]
    BPsyn = SACntw.BPsyn

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_position([0.1, 0.1, 0.7, 0.8])
    colrs = cmx.gist_rainbow(np.linspace(0, 1, len(celldata)))
    for i in range(len(celldata)):
        ax.scatter(celldata[i, 0], celldata[i, 1], s=celldata[i, 2],
                   c=0, alpha=0.5)

    for i in amac_rec:
        x = celldata[i, 0]
        y = celldata[i, 1]
        L = celldata[i, 2]
        ax.scatter(x, y, s=L,
                   c=colrs[i], alpha=0.8, label=labels[i])
        ax.plot([x - L, x + L], [y, y], '-', c=colrs[i])
        ax.plot([x, x], [y + L, y - L], '-', c=colrs[i])
        d = 0
        for dend in SACntw.amac[i].dend:
            synapse_per_seg = get_dendrite_synapses([BP[0] for BP in BPsyn],
                                                    dend)
            gaba_per_seg = get_dendrite_synapses(SACntw.gabasyn, dend)
            Lseg = dend.L / dend.nseg
            dend_angle = 2 * np.pi * d / len(SACntw.amac[i].dend)
            if d == 0 or d == 2:
                mrk = '|'
            else:
                mrk = '_'
            for j in range(dend.nseg):
                xs = np.cos(dend_angle) * np.linspace(j * Lseg,
                                                      (j + 1) * Lseg,
                                                      int(synapse_per_seg[j]))
                ys = np.sin(dend_angle) * np.linspace(j * Lseg,
                                                      (j + 1) * Lseg,
                                                      int(synapse_per_seg[j]))
                xsgaba = np.cos(dend_angle) * np.linspace(j * Lseg,
                                                          (j + 1) * Lseg,
                                                          int(gaba_per_seg[j]))
                ysgaba = np.sin(dend_angle) * np.linspace(j * Lseg,
                                                          (j + 1) * Lseg,
                                                          int(gaba_per_seg[j]))
                ax.scatter(xs + x * np.ones(len(xs)),
                           ys + y * np.ones(len(ys)),
                           marker=mrk,
                           c='k')
                ax.scatter(xsgaba + x * np.ones(len(xsgaba)),
                           ysgaba + y * np.ones(len(ysgaba)),
                           marker=mrk,
                           c='r')
            d += 1

    ax.legend(scatterpoints=1,
              loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=False, shadow=False, ncol=10, fontsize=8)

    ax.axis('scaled')
    plt.xlabel('x coordinate ($\mu$m)')
    plt.ylabel('y coordinate ($\mu$m)')
    import ntpath
    fn = (ntpath.basename(SACntw.celldatafilename).replace('.txt', '_') +
          ntpath.basename(SACntw.syndatafilename).replace('.txt', '_') +
          'subnetwork.png')
    plt.savefig(os.path.join(outfolder, fn), dpi=300, transparent=True)


def get_dendrite_synapses(syn_array, dendrite):
    nseg = dendrite.nseg
    segments = np.zeros(nseg)
    for syn in syn_array:
        if syn.get_segment().sec.name() == dendrite.name():
            segments[int(syn.get_segment().x * nseg)] += 1
    return segments
