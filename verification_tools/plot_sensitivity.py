"""
Properties that can be read out of plot_sensitivity:
'wavelengths', 'sns', 'lim_fluxes', 'sat_limits'
'line_limits' is also available for miri lrs and mrs
"""

import sys
import glob
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib.ticker import StrMethodFormatter


if len(sys.argv) > 1:
    prop = sys.argv[1]
else:
    print('Run this from the outputs folder.')
    print('Calling sequence: ')
    print('    python plot_sensitivity.py <property> <insnameA,modename1...> <insnameB,modename2...>')
    print('where <property> is sat_limits, lim_fluxes, or sns, and the instruments and modes are JWST ETC names')
    print('Or to get everything: ')
    print('    python plot_sensitivity.py <property>')
    print('Output is a .png file in the directory you\'re running this from.')
    raise ValueError("Need to specify the property argument.")
if len(sys.argv) > 2:
    insnames = sys.argv[2:]
else:
    insnames = ['miri,imaging,lrs,mrs', 'nircam,lw,sw', 'niriss,imaging,ami,soss,wfss', 'nirspec,fs,ifu,msa']

fig = plt.figure(figsize=(18,10))
ax = fig.add_subplot(111)
bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.7)

for instruments in insnames:
    instrument = instruments.split(',')[0]
    if instrument == "miri":
        # set up colors
        spectral = cm = plt.get_cmap('gist_heat_r')
        cNorm  = colors.Normalize(vmin=4.0, vmax=30)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        ax.plot(-1e-20,-1e-20,label='MIRI')
    elif instrument == "nircam":
        # set up colors
        spectral = cm = plt.get_cmap('OrRd')
        cNorm  = colors.Normalize(vmin=0.6, vmax=5.4)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        ax.plot(-1e-20,-1e-20,label='NIRCam')
    elif instrument == "niriss":
        # set up colors
        spectral = cm = plt.get_cmap('BuPu')
        cNorm  = colors.Normalize(vmin=0.7, vmax=5.4)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        ax.plot(-1e-20,-1e-20,label='NIRISS')
    elif instrument == "nirspec":
        # set up colors
        spectral = cm = plt.get_cmap('YlGn')
        cNorm  = colors.Normalize(vmin=0.7, vmax=5.4)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        ax.plot(-1e-20,-1e-20,label='NIRSpec')
    elif instrument == "wfirstimager":
        # set up colors
        spectral = cm = plt.get_cmap('Spectral_r')
        cNorm  = colors.Normalize(vmin=0.4, vmax=2)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        ax.plot(-1e-20,-1e-20,label='WFI')
    if prop == 'lim_fluxes':
        ylabel = 'Flux Density (S/N = 10 in 10000s) (microJy)'
        mult = 1e3
        ylim = (1e-2,1e5)
        yscale = 'log'
    elif prop == 'sat_limits':
        ylabel = 'Saturation Limit (Jy)'
        mult = 1e-3
        ylim = (1e-4,1e3)
        yscale = 'log'
    elif prop == 'sns':
        ylabel = 'Signal to Noise Ratio'
        mult = 1
        ylim = (3,3000)
        yscale = 'log'
    else:
        mult = 1
        ylabel = 'line_limits'
        ylim = (1e-23,1e-18)
        yscale = 'log'

    for mode in instruments.split(',')[1:]:
        data = np.load('{}_{}_sensitivity.npz'.format(instrument,mode))
        for x,keys in enumerate(data['configs']):
            colorVal = scalarMap.to_rgba(np.mean(data['wavelengths'][x]))
            if len(data['wavelengths'][x]) == 1:
                ax.scatter(data['wavelengths'][x],data[prop][x]*mult,label=data['configs'][x].values()[0], color=colorVal)
                ax.text(np.mean(data['wavelengths'][x]), (np.mean(data[prop][x])+(np.max(data[prop][x])/4.))*mult, data['configs'][x].values()[0], ha="center", va="bottom", bbox=bbox_props)
            else:
                vals = data[prop][x]
                vals[np.where(vals > 5e5)] = np.nan
                ax.plot(data['wavelengths'][x],vals*mult,label=data['configs'][x].values()[0], color=colorVal)
                ax.text(np.mean(data['wavelengths'][x]), np.nanmean(vals)*mult, data['configs'][x].values()[0], ha="center", va="bottom", bbox=bbox_props)
        data.close()
ax.set_xlabel('Wavelength (microns)')
ax.set_ylabel(ylabel)
ax.set_ylim(ylim)
ax.set_xscale('log')
ax.set_yscale(yscale)
ax.set_title(prop)
ax.xaxis.set_major_formatter(StrMethodFormatter('{x:g}'))
#ax.yaxis.set_major_formatter(StrMethodFormatter('{x:g}'))
plt.tight_layout()

plt.savefig('{}.png'.format(prop))
