import numpy as np
from verification_tools import calc_limits_extended

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
#apertures = 1.22*0.42*np.array([5.3,6.1,7.2,8.2,9.4,10.6,12.5,14.5,16.5,19.3,22.7,26.1])/10.
apertures = np.ones(12)*0.565
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
              'nint': 1,
              'nexp': 18
              }
strategy = {
            'target_xy': [0.0, 0.0],
            'method': 'ifunodinscene',
            'background_subtraction': False,
            'dithers': [{'x':-1,'y':-1},{'x':1,'y':1}]
            }

output = calc_limits_extended.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=150,skyfacs=1.05,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12',nflx=12)

np.savez('../../outputs/miri_mrs_sensitivity_extended.npz',
    wavelengths=output['wavelengths'], sns=output['sns'], lim_fluxes=output['lim_fluxes'],
    sat_limits=output['sat_limits'], configs=output['configs'], line_limits=output['line_limits'])
