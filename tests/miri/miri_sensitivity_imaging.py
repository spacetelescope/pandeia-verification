import numpy as np
from verification_tools import calc_limits

configs = [{'filter':'f560w'},
           {'filter':'f770w'},
           {'filter':'f1000w'},
           {'filter':'f1130w'},
           {'filter':'f1280w'},
           {'filter':'f1500w'},
           {'filter':'f1800w'},
           {'filter':'f2100w'},
           {'filter':'f2550w'}]

exp_configs = [{
                'subarray': 'full',
                'readout_pattern': 'fast',
                'ngroup': 106,
                'nint': 2,
                'nexp': 17
               },
               {
                'subarray': 'full',
                'readout_pattern': 'fast',
                'ngroup': 106,
                'nint': 2,
                'nexp':17
               },
               {
                 'subarray': 'full',
                 'readout_pattern': 'fast',
                 'ngroup': 106,
                 'nint': 2,
                 'nexp': 17
                },
                {
                'subarray': 'full',
                'readout_pattern': 'fast',
                'ngroup': 106,
                'nint': 2,
                'nexp': 17
                },
                {
                 'subarray': 'full',
                 'readout_pattern': 'fast',
                 'ngroup': 106,
                 'nint': 2,
                 'nexp': 17
                },
               {
                'subarray': 'full',
                'readout_pattern': 'fast',
                'ngroup': 22,
                'nint': 4,
                'nexp': 41
                },
                {
                 'subarray': 'full',
                 'readout_pattern': 'fast',
                 'ngroup': 22,
                 'nint': 4,
                 'nexp': 41
                },
                {
                'subarray': 'full',
                'readout_pattern': 'fast',
                'ngroup': 12,
                'nint': 15,
                'nexp': 20
                },
                {
                 'subarray': 'full',
                 'readout_pattern': 'fast',
                 'ngroup': 12,
                 'nint': 15,
                 'nexp': 20
                }
               ]

apertures = 0.42*np.array([5.6,7.7,10.,11.3,12.8,15.,18.,21.,25.5])/10.
idt_fluxes = np.array([0.16,0.25,0.54,1.35,0.84,1.39,3.46,7.09,26.2])*1e-3

obsmode = {
           'instrument': 'miri',
           'mode': 'imaging',
           'filter': None,
           'aperture': 'imager',
           'disperser': None
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'fast',
              'ngroup': 81,
              'nint': 40,
              'nexp': 1
              }
strategy = {
            'method': 'imagingapphot',
            'aperture_size': 1.1,
            'sky_annulus': [1.11,3.2],
            'target': [0.0, 0.0],
            'dithers': [{'x':0.0,'y':0.0}],
            'background_subtraction': False
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=50,skyfacs=1.,
                                 exp_configs=exp_configs,strategy=strategy,background='minzodi12')

np.savez('../../outputs/miri_imaging_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/miri_imaging_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
