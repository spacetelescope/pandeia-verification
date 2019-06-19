import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits
#from verification_tools import fudge_throughput as ft

configs = [{'filter':'r062','idt':70.00},
           {'filter':'z087','idt':120.00},
           {'filter':'y106','idt':120.00},
           {'filter':'j129','idt':120.00},
           {'filter':'w146','idt':70.00},
           {'filter':'h158','idt':120.00},
           {'filter':'f184','idt':200.00}
       ]


idt_fluxes = np.array([config['idt'] for config in configs])*1e-6
#wave_centers = np.array([2.5,2.77,3.0,3.22,3.23,3.35,3.56,3.60,4.05,4.10,4.18,4.30,4.44,4.60,4.66,4.70,4.80])
pixscale = 0.11  # arcsec
#diameter_flat_to_flat = 6.5 * 1e6 # meters to micron
#apertures = []
#for wave_center in wave_centers:
#    apertures.append(np.max([2.5*pixscale, (1.25 * (wave_center / diameter_flat_to_flat) *
#                     (180 * 3600 / np.pi))]))
apertures = np.array([2.5,2.5,2.5,2.5,2.5,2.5,2.5])*pixscale

obsmode = {
           'instrument': 'wfirstimager',
           'mode': 'imaging',
           'filter': 'r062',
           'aperture': 'any',
           'disperser': None
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'deep8',
              'ngroup': 5,
              'nint': 1,
              'nexp': 10
              }
strategy = {
            'method': 'imagingapphot',
            'aperture_size': 0.5,
            'sky_annulus': [0.6,3.2],
            'target': [0.0, 0.0],
            'dithers': [{'x':0.0,'y':0.0}],
            'background_subtraction': False
            }

output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=10,nflx=10,skyfacs=2.,
                                 exp_config=exp_config,strategy=strategy,background='wfirst_minzodi')
np.savez('../../outputs/wfirstimager_imager_sensitivity.npz',
    wavelengths=output['wavelengths'], sns=output['sns'], lim_fluxes=output['lim_fluxes'], sat_limits=output['sat_limits'], configs=output['configs'])
