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
    """
    Set some pretty default colors (a scale, a color for the legend, and an invisible plot for the legend)
    """
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
    """
    Klaus's sensitivity plots have specific labels and limits that need to be
    matched.

    Pretty much none of this matters for the comparison plots - labels, limits,
    and scale are ignored, and mult doesn't actually matter.
    """
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
    # The real important scale here: Percentage change
    ylabel = "% change ((old-new)/old)"
    return ylabel,mult,ylim,yscale

def gettext(data,x):
    """
    Text labels. Priority is: Disperser (and order) if it exists, then filter
    if it exists. If neither exist (unlikely), just use aperture.
    """
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
    """
    Imaging-like data, where each entry is a single filter point. Each needs to
    be labelled.
    This routine reads in the data and extracts the value, assigns the
    appropriate color to the point, and gets the text label and pastes it.
    """
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
    """
    Spectroscopy-like data, where each entry is a spectral bandpass. Compared to
    imaging modes, each will go into its own plot, so that can become the plot
    title. The actual spectral trace does not/should not be colored.

    Spectroscopic data is also only valid within certain limits, which this
    routine must read.
    """
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
    """
    Draw nice 10% boundaries on all the values with a colored rectangle polygon.

    Also set up the axes and labels - anything that needs to be done for both
    imaging and spectroscopic plots.
    """
    colorVal = scalarMap.to_rgba(np.mean([minx,maxx]))
    datax = np.linspace(minx,maxx,5)
    errpolyx = np.concatenate((datax,datax[::-1]))
    errpolyy = np.concatenate((np.ones_like(datax)*10, np.ones_like(datax)*-10))
    poly = Polygon(list(zip(errpolyx,errpolyy)), closed=True)
    patch = PatchCollection([poly], alpha=0.3, color=colorVal)
    ax.add_collection(patch)

    ax.set_xlabel('Wavelength (microns)')
    ax.set_ylabel(ylabel)
    # the boundaries of the acceptable rectangle are +/- 10% but that's prone to
    # obscuring small but interesting differences. Make the minimum size +/- 5%.
    miny,maxy = ax.get_ylim()
    if miny > -5:
        miny = -5
    if maxy < 5:
        maxy = 5
    ax.set_ylim(miny,maxy)
    ax.set_xlim(minx-0.1,maxx+0.1)
    ax.get_xaxis().set_major_formatter(StrMethodFormatter('{x:g}'))
    ax.grid()
    return ax

"""
The main routine: read in input to determine what to plot.
"""


if len(sys.argv) > 1:
    PROP = sys.argv[1]
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

# The plot is going to have at least 9 subplots, so it had better be huge
fig = plt.figure(figsize=(20,20))
# set up a nice label for the points
bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.7)

# Set up plot parameters (range, scale, ylabel)
ylabel,mult,ylim,yscale = plotparams(prop)

# legend is unused in this code
legendhandles = []

# How many subplots do we need? An imaging mode gets only one, but a
# spectroscopic mode should get one per setup.
subplots = 0
for instruments in insnames:
    instrument = instruments.split(',')[0]

    for mode in instruments.split(',')[1:]:
        data = np.load('../outputs/{}_{}_sensitivity.npz'.format(instrument,mode))
        toadd = 0
        for x,keys in enumerate(data['configs']):
            if len(data['wavelengths'][x]) == 1:
                toadd = 1
            else:
                toadd += 1
        subplots += toadd

for instruments in insnames:
    instrument = instruments.split(',')[0]
    # Now that we know how many subplots we need, make a grid with enough plots.
    ax = fig.subplots(nrows=np.int(np.ceil(subplots/3.)),ncols=3)
    # This sets up the legend and the color scheme based on the instrument
    scalarMap,legendhandles,ax = setup(instrument,ax)

    # go back through the modes again, and plot in the correct cells.
    num = 0
    for mode in instruments.split(',')[1:]:
        data = np.load('../outputs/{}_{}_sensitivity.npz'.format(instrument,mode))
        data2 = np.load('../latest/{}_{}_sensitivity.npz'.format(instrument,mode))
        print(instrument,mode)
        if len(data['wavelengths'][0]) == 1:
            # If the mode is imaging data, we need to put all the data values on
            # one plot
            waves = []
            for x,keys in enumerate(data['configs']):
                # compareone will handle all the aspects of plotting the point
                ax[num/3][num%3], wave = compareone(data, data2, x, ax[num/3][num%3], scalarMap)
                waves.append(wave)
            # add the title and the boundary rectangle
            ax[num/3][num%3].set_title('{} {}'.format(instrument.upper(),mode.upper()))
            ax[num/3][num%3] = drawbounds(np.min(waves),np.max(waves), ax[num/3][num%3], scalarMap)
            num += 1
        else:
            # if the mode is spectroscopic data, we need to put each setup in
            # its own plot
            for x,keys in enumerate(data['configs']):
                # comparemulti will handle all aspects of plotting the spectrum
                ax[num/3][num%3], wave = comparemulti(data, data2, x, ax[num/3][num%3], scalarMap, instrument, mode)
                ax[num/3][num%3] = drawbounds(np.min(wave), np.max(wave), ax[num/3][num%3], scalarMap)
                num += 1


        data.close()
        data2.close()

# Add a global title to the plot - it's probably going to be in a weird place,
# so make it prominent.
fig.suptitle('{}'.format(prop.upper()), fontsize="x-large", fontstyle="italics")
plt.tight_layout()

# save the plot
plt.savefig('{}.png'.format(prop))
