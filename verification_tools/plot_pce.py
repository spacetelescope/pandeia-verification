import matplotlib.pylab as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, ScalarFormatter

from get_pce import *

"""
Method to plot the system throughput of a Pandeia instrument/mode/element combination.
The arguments use the Pandeia naming conventions.

Arguments:
---------
instrument: string
    Name of the Pandeia instrument.
mode: string
    Name of the mode of the instrument

Keywords:
--------
config: list
    List of dictionaries of instrument configurations to be extracted and plotted.
outfile: string
    Name of the plot file. As usual with matplotlib, the surname defines the image format.
wrange: tuple
    Wavelength range to be plotted.

"""
def plot_pce(instrument,mode,configs=None,outfile='plot.pdf',wrange=(0.5,5.5),yrange=None,
             label_types=['filter'],logwave=False, filetype='png',comparisons=None, scale_pce=None):

    # create figure, assign size
    f,ax = plt.subplots(1,sharex=True,sharey=True)
    f.set_size_inches(11.5,4.5)

    # set up colors
    spectral = cm = plt.get_cmap('Spectral')
    cNorm  = colors.Normalize(vmin=wrange[0], vmax=wrange[1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=spectral)

    # set up minor tick marks
    XminorLocator = MultipleLocator(0.1)
    YminorLocator = MultipleLocator(0.1)

    for config in configs:
        wave,pce = get_pce(instrument,mode,config)
        if scale_pce is not None:
            pce *= np.interp(wave,scale_pce['wave'],scale_pce['throughput'])

        name = ''
        for label in label_types:
            name=name+config[label]+'\n'

        # find the midpoint of the area with the transmission > 50%
        # put the filter label in that location
        maxthrough = np.max(pce)
        upthrough = pce > 0.005
        midpt = np.median(wave[upthrough])
        colorVal = scalarMap.to_rgba(np.mean(wave[upthrough]))
        ax.plot(wave,pce,color=colorVal)
        ax.fill_between(wave,0,pce,color=colorVal,alpha=0.5)
        ax.text(midpt,maxthrough*1.1,
                name.upper(),color='black',fontsize=10,ha='center')

    # Use a logarithmic x-axis?
    if logwave:
        ax.set_xscale('log')
        ax.xaxis.set_major_formatter(ScalarFormatter())

    # limit the number of y-ticks
    ax.set_yticks([0, 0.5, 1])
    ax.yaxis.set_minor_locator(YminorLocator)

    # x range and ticks
    ax.set_xlim(wrange[0],wrange[1])
    ax.set_xticks(np.linspace(wrange[0],wrange[1],5))
    ax.xaxis.set_minor_locator(XminorLocator)

    if yrange is not None:
        ax.set_ylim(yrange[0],yrange[1])
        ax.set_yticks(np.linspace(yrange[0],yrange[1],5))
        ax.yaxis.set_minor_locator(YminorLocator)

    ax.set_xlabel('Wavelength [$\mu$m]')
    ax.set_ylabel('Photon-to-electron conversion efficiency')

    if comparisons is not None:
        for comparison in comparisons:
            wave = comparison[0]
            pce = comparison[1]
            maxthrough = np.max(pce)
            upthrough = pce > 0.003
            midpt = np.median(wave[upthrough])
            colorVal = scalarMap.to_rgba(np.mean(wave[upthrough]))
            ax.plot(comparison[0],comparison[1],linestyle='--',color=colorVal)

    plt.tight_layout()

    f.savefig(outfile+'.'+filetype,clobber=True)
