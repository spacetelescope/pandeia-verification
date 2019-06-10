import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits

configs = [{'filter':'f070w','idt':21.81},
           {'filter':'f090w','idt':15.07},
           {'filter':'f115w','idt':12.99},
           {'filter':'f150w','idt':10.68},
           {'filter':'f200w','idt':9.34},
           {'filter':'f140m','idt':19.17},
           {'filter':'f162m','idt':18.07},
           {'filter':'f182m','idt':14.13},
           {'filter':'f210m','idt':17.26},
           {'filter':'f164n','idt':139.98},
           {'filter':'f187n','idt':136.41},
           {'filter':'f212n','idt':127.27}]

idt_fluxes = np.array([config['idt'] for config in configs])*1e-6
pixscale = 0.0317  # arcsec
apertures = np.array([2.652,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.62])*pixscale
obsmode = {
           'instrument': 'nircam',
           'mode': 'sw_imaging',
           'filter': 'f070w',
           'aperture': 'sw',
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
            'aperture_size': 1.1,
            'sky_annulus': [1.11,3.2],
            'target': [0.0, 0.0],
            'dithers': [{'x':0.0,'y':0.0}],
            'background_subtraction': False
            }

output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=10,nflx=10,skyfacs=2.,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')


np.savez('../../outputs/nircam_sw_sensitivity.npz',
    wavelengths=output['wavelengths'], sns=output['sns'], lim_fluxes=output['lim_fluxes'], sat_limits=output['sat_limits'], configs=output['configs'])
