import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits

configs = [{'aperture':'imager','mode':'lrsslitless'},
           {'aperture':'lrsslit','mode':'lrsslit'}]
apertures = np.array([0.84,0.84])*7.5/10.
idt_fluxes = np.array([5e-3,30e-3])

obsmode = {
           'instrument': 'miri',
           'mode': 'lrsslit',
           'filter': None,
           'aperture': 'lrsslit',
           'disperser': 'p750l'
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'fast',
              'ngroup': 180,
              'nint': 1,
              'nexp': 20
              }
strategy = {
            'method': 'specapphot',
            'aperture_size': 1.1,
            'sky_annulus': [1.11,3.2],
            'background_subtraction': False
            }


output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=1000,nflx=80,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/miri_lrs_sensitivity.npz',
    wavelengths=output[0]['wavelengths'], sns=output[0]['sns'], lim_fluxes=output[0]['lim_fluxes'],
    source_rates_per_njy=output[0]['source_rates_per_njy'], sat_limits=output[0]['sat_limits'], configs=output[0]['configs'], line_limits=output[0]['line_limits'])

np.savez('../../outputs/miri_lrs_sensitivity_one.npz',
    wavelengths=output[1]['wavelengths'], sns=output[1]['sns'], lim_fluxes=output[1]['lim_fluxes'],
    source_rates_per_njy=output[1]['source_rates_per_njy'], sat_limits=output[1]['sat_limits'], configs=output[1]['configs'], line_limits=output[1]['line_limits'])
