import numpy as np
from verification_tools import calc_limits

configs = [{'aperture':'ch1','disperser':'short'},
           {'aperture':'ch1','disperser':'medium'},
           {'aperture':'ch1','disperser':'long'},
           {'aperture':'ch2','disperser':'short'},
           {'aperture':'ch2','disperser':'medium'},
           {'aperture':'ch2','disperser':'long'},
           {'aperture':'ch3','disperser':'short'},
           {'aperture':'ch3','disperser':'medium'},
           {'aperture':'ch3','disperser':'long'},
           {'aperture':'ch4','disperser':'short'},
           {'aperture':'ch4','disperser':'medium'},
           {'aperture':'ch4','disperser':'long'}]
apertures = 1.22*0.42*np.array([5.3,6.1,7.2,8.2,9.4,10.6,12.5,14.5,16.5,19.3,22.7,26.1])/10.
idt_fluxes = np.array([0.05,0.043,0.046,0.045,0.051,0.060,0.098,0.084,0.136,0.54,1.2,2.9])

obsmode = {
           'instrument': 'miri',
           'mode': 'mrs',
           'filter': None,
           'aperture': 'ch1',
           'disperser': 'short'
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'fast',
              'ngroup': 99,
              'nint': 18,
              'nexp': 1
              }
strategy = {
            'target_xy': [0.0, 0.0],
            'method': 'ifunodinscene',
            'aperture_size': 1.1,
            'dithers': [{'x':0,'y':0},{'x':1,'y':1}],
            "units": "arcsec"
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=150,skyfacs=1.05,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/miri_mrs_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'],
    sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'], line_limits=outputs_regular['line_limits'])

np.savez('../../outputs/miri_mrs_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'],
    sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'], line_limits=outputs_one['line_limits'])
