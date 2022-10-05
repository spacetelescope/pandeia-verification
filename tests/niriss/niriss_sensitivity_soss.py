import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits

configs = [{'aperture':'soss','filter':'clear','disperser':'gr700xd'},
           {'aperture':'soss','filter':'clear','disperser':'gr700xd'}]

apertures = np.array([2.5,2.5])*0.0656
idt_fluxes = np.array([0.03, 0.03])
orders = [1,2]
obsmode = {
           'instrument': 'niriss',
           'mode': 'soss',
           'filter': 'clear',
           'aperture': 'soss',
           'disperser': 'gr700xd'
           }
exp_config = {
              'subarray': 'substrip256',
              'readout_pattern': 'nisrapid',
              'ngroup': 36,
              'nint': 1,
              'nexp': 5
              }
strategy = {
            'method': 'soss',
            'order': 1
            }

output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=1000,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12',orders=orders)

np.savez('../../outputs/niriss_soss_sensitivity.npz',
    wavelengths=output[0]['wavelengths'], sns=output[0]['sns'], lim_fluxes=output[0]['lim_fluxes'], sat_limits=output[0]['sat_limits'], configs=output[0]['configs'], orders=output[0]['orders'])

np.savez('../../outputs/niriss_soss_sensitivity_one.npz',
    wavelengths=output[1]['wavelengths'], sns=output[1]['sns'], lim_fluxes=output[1]['lim_fluxes'], sat_limits=output[1]['sat_limits'], configs=output[1]['configs'], orders=output[1]['orders'])
