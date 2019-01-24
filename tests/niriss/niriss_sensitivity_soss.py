import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits

configs = [{'aperture':'soss','filter':None,'disperser':'gr700xd'},
           {'aperture':'soss','filter':None,'disperser':'gr700xd'}]
     
apertures = np.array([2.5,2.5])*0.0656
idt_fluxes = np.array([0.03, 0.03])
orders = [1,2]
obsmode = {
           'instrument': 'niriss',
           'mode': 'soss',
           'filter': None,
           'aperture': 'soss',
           'disperser': 'gr700xd'
           }
exp_config = {
              'subarray': 'substrip256',
              'readmode': 'nisrapid',
              'ngroup': 36,
              'nint': 1,
              'nexp': 5
              }
strategy = {
            'method': 'soss',
            'order': 1
            }
    
output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=20,nflx=10,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12',orders=orders)

np.savez('../../outputs/niriss_soss_sensitivity.npz',
    wavelengths=output['wavelengths'], sns=output['sns'], lim_fluxes=output['lim_fluxes'], sat_limits=output['sat_limits'], configs=output['configs'], orders=output['orders'])