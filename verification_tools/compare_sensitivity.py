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
from matplotlib.patches import Polygon
from matplotlib.ticker import StrMethodFormatter
from matplotlib.collections import PatchCollection


def setup(instrument, ax):
    if instrument == "miri":
        # set up colors
        spectral = cm = plt.get_cmap('gist_heat_r')
        cNorm  = colors.Normalize(vmin=4.0, vmax=30)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        # for whatever reason, line plot artists are actually lists of artists
        # unlike every other type of plot I've seen.
        colorVal = scalarMap.to_rgba(17)
        miri = ax[0][0].plot(-1e-20,-1e-20,label='MIRI', color=colorVal)
        legendhandles.append(miri[0])
    elif instrument == "nircam":
        # set up colors
        spectral = cm = plt.get_cmap('cool')
        cNorm  = colors.Normalize(vmin=0.6, vmax=5.4)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        colorVal = scalarMap.to_rgba(3)
        nircam = ax[0][0].plot(-1e-20,-1e-20,label='NIRCam', color=colorVal)
        legendhandles.append(nircam[0])
    elif instrument == "niriss":
        # set up colors
        spectral = cm = plt.get_cmap('autumn')
        cNorm  = colors.Normalize(vmin=0.7, vmax=5.4)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        colorVal = scalarMap.to_rgba(3)
        niriss = ax[0][0].plot(-1e-20,-1e-20,label='NIRISS', color=colorVal)
        legendhandles.append(niriss[0])
    elif instrument == "nirspec":
        # set up colors
        spectral = cm = plt.get_cmap('YlGn')
        cNorm  = colors.Normalize(vmin=0.7, vmax=5.4)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        colorVal = scalarMap.to_rgba(3)
        nirspec = ax[0][0].plot(-1e-20,-1e-20,label='NIRSpec', color=colorVal)
        legendhandles.append(nirspec[0])
    elif instrument == "wfirstimager":
        # set up colors
        spectral = cm = plt.get_cmap('Spectral_r')
        cNorm  = colors.Normalize(vmin=0.4, vmax=2)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)
        colorVal = scalarMap.to_rgba(1)
        wfirstimager = ax[0][0].plot([0.6, 2],[-1e-20,-1e-20],label='WFIRST Imager', color=colorVal)
        legendhandles.append(wfirstimager[0])

    return scalarMap,legendhandles, ax

def plotparams(prop):
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
    ylabel = "% change ((old-new)/old)"
    return ylabel,mult,ylim,yscale

def gettext(data,x):
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
    return textval

def compareone(data, data2, x, ax, scalarMap):
    colorVal = scalarMap.to_rgba(np.mean(data['wavelengths'][x]))
    wave = data['wavelengths'][x]
    vals = data[prop][x]*mult
    vals2 = data2[prop][x]*mult
    textval = gettext(data,x)
    ydata = ((vals-vals2)/vals)*100
    ax.scatter(wave,ydata, color=colorVal)
    # the modulus makes it either 0 or 1, the rest of the code is to flip the label above or below the point
    ax.text(np.mean(wave), ydata - (x%2-0.5)*2, textval.upper(), ha="center", va="bottom", bbox=bbox_props)

    return ax, wave

def comparemulti(data, data2, x, ax, scalarMap, instrument, mode):
    colorVal = scalarMap.to_rgba(np.mean(data['wavelengths'][x]))
    wave = data['wavelengths'][x]
    vals = data[prop][x]*mult
    vals2 = data2[prop][x]*mult
    textval = gettext(data,x)
    if 'bounds' in keys.keys():
        bounds = data['configs'][x]['bounds']
        gsubs = np.where((wave>bounds[0]) & (wave<bounds[1]))
    else:
        if instrument == 'nirspec' and prop == 'sat_limits':
            gsubs = np.where(vals*mult < 7)
        else:
            gsubs = np.where(vals > -6)
    ax.plot(wave[gsubs], ((vals[gsubs]-vals2[gsubs])/vals[gsubs])*100, color='#000000', linewidth=3)
    ax.set_title("{} {} {}".format(instrument.upper(), mode.upper(), textval.upper()))

    return ax, wave

def drawbounds(minx,maxx,ax, scalarMap):
    colorVal = scalarMap.to_rgba(np.mean([minx,maxx]))
    datax = np.linspace(minx,maxx,5)
    errpolyx = np.concatenate((datax,datax[::-1]))
    errpolyy = np.concatenate((np.ones_like(datax)*10, np.ones_like(datax)*-10))
    poly = Polygon(list(zip(errpolyx,errpolyy)), closed=True)
    patch = PatchCollection([poly], alpha=0.3, color=colorVal)
    ax.add_collection(patch)
    ax.set_xlabel('Wavelength (microns)')
    ax.set_ylabel(ylabel)
    miny,maxy = ax.get_ylim()
    if miny > -5:
        miny = -5
    if maxy < 5:
        maxy = 5
    ax.set_ylim(miny,maxy)
    ax.set_xlim(minx-0.1,maxx+0.1)
    #ax.set_xscale('log')
    #ax.set_xticks([0.6, 1, 2, 5, 10, 15, 20, 25])
    ax.get_xaxis().set_major_formatter(StrMethodFormatter('{x:g}'))
    ax.grid()
    return ax

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

fig = plt.figure(figsize=(20,20))
bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.7)

legendhandles = []

ylabel,mult,ylim,yscale = plotparams(prop)

for instruments in insnames:
    instrument = instruments.split(',')[0]

    subplots = 0
    for mode in instruments.split(',')[1:]:
        data = np.load('../outputs/{}_{}_sensitivity.npz'.format(instrument,mode))
        toadd = 0
        for x,keys in enumerate(data['configs']):
            if len(data['wavelengths'][x]) == 1:
                toadd = 1
            else:
                toadd += 1
        subplots += toadd

    ax = fig.subplots(nrows=np.int(np.ceil(subplots/3.)),ncols=3)
    scalarMap,legendhandles,ax = setup(instrument,ax)

    num = 0
    for mode in instruments.split(',')[1:]:
        data = np.load('../outputs/{}_{}_sensitivity.npz'.format(instrument,mode))
        data2 = np.load('../latest/{}_{}_sensitivity.npz'.format(instrument,mode))
        print(instrument,mode)
        if len(data['wavelengths'][0]) == 1:
            waves = []
            for x,keys in enumerate(data['configs']):

                ax[num/3][num%3], wave = compareone(data, data2, x, ax[num/3][num%3], scalarMap)
                waves.append(wave)
            ax[num/3][num%3].set_title('{} {}'.format(instrument.upper(),mode.upper()))
            ax[num/3][num%3] = drawbounds(np.min(waves),np.max(waves), ax[num/3][num%3], scalarMap)
            num += 1
        else:
            for x,keys in enumerate(data['configs']):
                ax[num/3][num%3], wave = comparemulti(data, data2, x, ax[num/3][num%3], scalarMap, instrument, mode)
                ax[num/3][num%3] = drawbounds(np.min(wave), np.max(wave), ax[num/3][num%3], scalarMap)
                num += 1


        data.close()

fig.suptitle('{}'.format(prop.upper()))
plt.tight_layout()

plt.savefig('{}.png'.format(prop))
