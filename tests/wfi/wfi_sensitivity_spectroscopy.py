import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits
#from verification_tools import fudge_throughput as ft

configs = [{'aperture':'spectroscopy', 'filter':None, 'disperser':'g150', 'bounds':(1.0,1.93)},
           {'aperture':'spectroscopy', 'filter':None, 'disperser':'p120', 'bounds':(0.76,1.8)}]

apertures = np.array([5,5,5,5,5,5,5,5,5,5,5,5])*0.11
idt_fluxes = np.array([1e-2, 1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2])
skyfacs = [2,2,2,2,2,2,2,2,2,2,2,2]
obsmode = {
           'instrument': 'wfi',
           'mode': 'spectroscopy',
           'filter': None,
           'aperture': 'spectroscopy',
           'disperser': 'g150'
           }
exp_config = {
              'subarray': 'spectroscopy',
              'readout_pattern': 'deep8',
              'ngroup': 5,
              'nint': 1,
              'nexp': 10
              }
strategy = {
            'method': 'specapphot',
            'aperture_size': 0.15,
            'sky_annulus': [0.16,0.5],
            'background_subtraction': False
            }

output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=50,skyfacs=skyfacs,
                                 exp_config=exp_config,strategy=strategy,background='roman_minzodi')

np.savez('../../outputs/wfi_spectroscopy_sensitivity.npz',
    wavelengths=output['wavelengths'], sns=output['sns'], lim_fluxes=output['lim_fluxes'], sat_limits=output['sat_limits'], configs=output['configs'])
