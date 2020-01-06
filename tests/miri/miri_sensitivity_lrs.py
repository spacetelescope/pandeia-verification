import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits

configs = [{'aperture':'imager','mode':'lrsslitless'},
           {'aperture':'lrsslit','mode':'lrsslit'}]
apertures = np.array([0.42,0.42])*7.5/10.
idt_fluxes = np.array([5e-2,30e-3])

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


output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=100,nflx=20,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/miri_lrs_sensitivity.npz',
    wavelengths=output['wavelengths'], sns=output['sns'], lim_fluxes=output['lim_fluxes'],
    source_rates_per_njy=output['source_rates_per_njy'], sat_limits=output['sat_limits'], configs=output['configs'], line_limits=output['line_limits'])
