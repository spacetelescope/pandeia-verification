import matplotlib.pylab as plt
import numpy as np
import astropy.io.ascii as at
from verification_tools import plot_pce as pp

filetype = 'pdf'

idt_pce = at.read('../../benchmarks/LRSPCE_TN-00072-ATC-Iss1.csv',data_start=2)
#import pdb;pdb.set_trace()
wave = idt_pce['Wavelength'].data
pce = idt_pce['Enslitted PCE'].data

miri_lrs_sens = np.load('../../outputs/miri_lrs_sensitivity.npz')
slitloss = miri_lrs_sens['source_rates_per_njy'][1]/miri_lrs_sens['source_rates_per_njy'][0]

comparisons = [[wave,pce]]

configs = [{'aperture':'imager','filter':None,'disperser':'p750l'}]

#import pdb;pdb.set_trace()
pp.plot_pce('miri','lrsslit',configs,wrange=(4.,15),yrange=(0,0.5),outfile='../../plots/miri_lrs_pce',
            label_types=['disperser'],filetype=filetype,comparisons=comparisons,scale_pce={'wave':miri_lrs_sens['wavelengths'][0],'throughput':slitloss})

