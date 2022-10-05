import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits

configs = [{'filter':'f277w','idt':200.0},
           {'filter':'f380m','idt':200.0},
           {'filter':'f430m','idt':200.0},
           {'filter':'f480m','idt':400.0}
       ]

idt_fluxes = np.array([config['idt'] for config in configs])*1e-6
apertures = []
apertures = np.array([2.5,2.5,2.72,2.72])*0.0646

obsmode = {
           'instrument': 'niriss',
           'mode': 'ami',
           'filter': 'f277w',
           'aperture': 'nrm',
           'disperser': None
           }
exp_config = {
              'subarray': 'sub80',
              'readout_pattern': 'nisrapid',
              'ngroup': 133,
              'nint': 10,
              'nexp': 100
              }
strategy = {
            'method': 'imagingapphot',
            'aperture_size': 1.1,
            'sky_annulus': [1.11,3.2],
            'target': [0.0, 0.0],
            'background_subtraction': False
            }

output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=100,skyfacs=3.,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/niriss_ami_sensitivity.npz',
    wavelengths=output[0]['wavelengths'], sns=output[0]['sns'], lim_fluxes=output[0]['lim_fluxes'], sat_limits=output[0]['sat_limits'], configs=output[0]['configs'])

np.savez('../../outputs/niriss_ami_sensitivity_one.npz',
    wavelengths=output[1]['wavelengths'], sns=output[1]['sns'], lim_fluxes=output[1]['lim_fluxes'], sat_limits=output[1]['sat_limits'], configs=output[1]['configs'])
