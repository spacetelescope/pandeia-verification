import os
import matplotlib.pylab as plt
import numpy as np
import astropy.io.ascii as at
import astropy.io.fits as fits
from verification_tools import plot_pce as pp

filetype = 'pdf'

#idt_pce = at.read('../../benchmarks/ImPCE_TN-00072-ATC-Iss1.csv')
path = '../../benchmarks/MIRI_CDP6/'
idt_pces = ['MIRI_FM_MIRIMAGE_F560W_PCE_06.00.00.fits',
            'MIRI_FM_MIRIMAGE_F770W_PCE_06.00.00.fits',
            'MIRI_FM_MIRIMAGE_F1000W_PCE_06.00.00.fits',
            'MIRI_FM_MIRIMAGE_F1130W_PCE_06.00.00.fits',
            'MIRI_FM_MIRIMAGE_F1280W_PCE_06.00.00.fits',
            'MIRI_FM_MIRIMAGE_F1500W_PCE_06.00.00.fits',
            'MIRI_FM_MIRIMAGE_F1800W_PCE_06.00.00.fits',
            'MIRI_FM_MIRIMAGE_F2100W_PCE_06.00.00.fits',
            'MIRI_FM_MIRIMAGE_F2550W_PCE_06.00.00.fits']         
         
idt_pce = fits.getdata('../../benchmarks/MIRI_CDP6/MIRI_FM_MIRIMAGE_F1000W_PCE_06.00.00.fits')
filters = ['f560w','f770w','f1000w','f1130w','f1280w','f1500w','f1800w','f2100w','f2550w']
configs = [{'filter':filter,'disperser':None,'aperture':'imager'} for filter in filters]

comparisons = []
for filter,idt_pce in zip(filters,idt_pces):
    data = fits.getdata(os.path.join(path,idt_pce))
    comparison = [data['wavelength'],data['efficiency']]
    comparisons.append(comparison)

pp.plot_pce('miri','imaging',configs,wrange=(4.,31),yrange=(0,0.5),outfile='../../plots/miri_imaging_pce',
            label_types=['filter'],filetype=filetype,comparisons=comparisons)

