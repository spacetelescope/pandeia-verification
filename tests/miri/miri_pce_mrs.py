import matplotlib.pylab as plt
import numpy as np
import astropy.io.ascii as at
from verification_tools import plot_pce as pp

filetype = 'pdf'

idt_pce = at.read('../../benchmarks/MRSPCE_TN-00072-ATC-Iss1.csv',data_start=2)

modules = idt_pce['Sub-band'].data
wave = idt_pce['Wavelength'].data
pce = idt_pce['PCE'].data

comparisons = []
for module in np.unique(modules):
    gs = np.where(module==modules)
    comparison = [wave[gs],pce[gs]]
    comparisons.append(comparison)


configs = [{'aperture':'ch1','disperser':'short','filter':None},
           {'aperture':'ch1','disperser':'medium','filter':None},
           {'aperture':'ch1','disperser':'long','filter':None},
           {'aperture':'ch2','disperser':'short','filter':None},
           {'aperture':'ch2','disperser':'medium','filter':None},
           {'aperture':'ch2','disperser':'long','filter':None},
           {'aperture':'ch3','disperser':'short','filter':None},
           {'aperture':'ch3','disperser':'medium','filter':None},
           {'aperture':'ch3','disperser':'long','filter':None},
           {'aperture':'ch4','disperser':'short','filter':None},
           {'aperture':'ch4','disperser':'medium','filter':None},
           {'aperture':'ch4','disperser':'long','filter':None}]

pp.plot_pce('miri','mrs',configs,wrange=(4.,30),yrange=(0,0.2),outfile='../../plots/miri_mrs_pce',
            label_types=['aperture'],filetype=filetype,comparisons=comparisons)

