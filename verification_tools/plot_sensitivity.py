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
    insnames = ['miri,imaging,lrs,mrs', 'nircam,lw,sw,wfgrism', 'niriss,imaging,ami,soss,wfss', 'nirspec,fs,ifu,msa']

fig = plt.figure(figsize=(20,12))
ax = fig.add_subplot(111)
bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.7)

legendhandles = []

for instruments in insnames:
    instrument = instruments.split(',')[0]
    if instrument == "miri":
        # set up colors
        spectral = cm = plt.get_cmap('gist_heat_r')
        cNorm  = colors.Normalize(vmin=4.0, vmax=30)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        # for whatever reason, line plot artists are actually lists of artists
        # unlike every other type of plot I've seen.
        colorVal = scalarMap.to_rgba(17)
        miri = ax.plot(-1e-20,-1e-20,label='MIRI', color=colorVal)
        legendhandles.append(miri[0])
    elif instrument == "nircam":
        # set up colors
        spectral = cm = plt.get_cmap('cool')
        cNorm  = colors.Normalize(vmin=0.6, vmax=5.4)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        colorVal = scalarMap.to_rgba(3)
        nircam = ax.plot(-1e-20,-1e-20,label='NIRCam', color=colorVal)
        legendhandles.append(nircam[0])
    elif instrument == "niriss":
        # set up colors
        spectral = cm = plt.get_cmap('autumn')
        cNorm  = colors.Normalize(vmin=0.7, vmax=5.4)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        colorVal = scalarMap.to_rgba(3)
        niriss = ax.plot(-1e-20,-1e-20,label='NIRISS', color=colorVal)
        legendhandles.append(niriss[0])
    elif instrument == "nirspec":
        # set up colors
        spectral = cm = plt.get_cmap('YlGn')
        cNorm  = colors.Normalize(vmin=0.7, vmax=5.4)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        colorVal = scalarMap.to_rgba(3)
        nirspec = ax.plot(-1e-20,-1e-20,label='NIRSpec', color=colorVal)
        legendhandles.append(nirspec[0])
    elif instrument == "wfirstimager":
        # set up colors
        spectral = cm = plt.get_cmap('Spectral_r')
        cNorm  = colors.Normalize(vmin=0.4, vmax=2)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        wfirstimager = ax.plot([0.6, 2],[-1e-20,-1e-20],label='WFIRST Imager')
        legendhandles.append(wfirstimager[0])
    if prop == 'lim_fluxes':
        ylabel = 'Flux Density (S/N = 10 in 10000s) (microJy)'
        mult = 1e3
        ylim = (1e-3,5e4)
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
        data = np.load('../outputs/{}_{}_sensitivity.npz'.format(instrument,mode))
        print(instrument,mode)
        for x,keys in enumerate(data['configs']):
            colorVal = scalarMap.to_rgba(np.mean(data['wavelengths'][x]))
            # get text
            if 'disperser' in data['configs'][x]:
                if 'filter' in data['configs'][x]:
                    if data['configs'][x]['filter'] == None:
                        textval = '{} {}'.format(data['configs'][x]['disperser'], data['orders'][x])
                    else:
                        textval = '{} {}'.format(data['configs'][x]['disperser'], data['configs'][x]['filter'])
                else:
                    textval = '{} {}'.format(data['configs'][x]['aperture'],data['configs'][x]['disperser'])
            else:
                if 'filter' in data['configs'][x]:
                    textval = data['configs'][x]['filter']
                else:
                    textval = data['configs'][x]['aperture']

            if len(data['wavelengths'][x]) == 1:
                ax.scatter(data['wavelengths'][x],data[prop][x]*mult,label=data['configs'][x].values()[0], color=colorVal)
                ax.text(np.mean(data['wavelengths'][x]), (np.mean(data[prop][x])+(np.max(data[prop][x])/4.))*mult, textval, ha="center", va="bottom", bbox=bbox_props)
            else:
                wave = data['wavelengths'][x]
                vals = data[prop][x]
                if 'bounds' in keys.keys():
                    bounds = data['configs'][x]['bounds']
                    gsubs = np.where((wave>bounds[0]) & (wave<bounds[1]))
                else:
                    if instrument == 'nirspec' and prop == 'sat_limits':
                        gsubs = np.where(vals*mult < 7)
                    else:
                        gsubs = np.where(vals > -6)
                ax.plot(wave[gsubs],vals[gsubs]*mult,label=data['configs'][x].values()[0], color=colorVal)
                ax.text(np.mean(wave[gsubs]), np.nanmedian(vals[gsubs])*mult, textval, ha="center", va="bottom", bbox=bbox_props)
        data.close()
ax.set_xlabel('Wavelength (microns)')
ax.set_ylabel(ylabel)
ax.set_xscale('log')
ax.set_xticks([0.6, 1, 2, 5, 10, 15, 20, 25])
ax.get_xaxis().set_major_formatter(StrMethodFormatter('{x:g}'))
ax.set_ylim(ylim)
ax.set_yscale(yscale)
ax.set_title(prop)
ax.grid()
ax.legend(handles=legendhandles)
#ax.yaxis.set_major_formatter(StrMethodFormatter('{x:g}'))
plt.tight_layout()

plt.savefig('{}.png'.format(prop))
