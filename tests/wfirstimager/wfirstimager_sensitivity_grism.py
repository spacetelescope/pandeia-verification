import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits
#from verification_tools import fudge_throughput as ft

configs = [{'aperture':'grism','filter':'g150','disperser':'grsgrism','bounds':(0.95,1.9)}]

apertures = np.array([2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5])*0.11
idt_fluxes = np.array([1e-2, 1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2])
skyfacs = [2,2,2,2,2,2,2,2,2,2,2,2]
obsmode = {
           'instrument': 'wfirstimager',
           'mode': 'grism',
           'filter': 'g150',
           'aperture': 'grism',
           'disperser': 'grsgrism'
           }
exp_config = {
              'subarray': 'full',
              'readmode': 'deep8',
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

output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=5,skyfacs=skyfacs,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/wfirst_wfirstgrism_sensitivity.npz',
    wavelengths=output['wavelengths'], sns=output['sns'], lim_fluxes=output['lim_fluxes'], sat_limits=output['sat_limits'], configs=output['configs'])
