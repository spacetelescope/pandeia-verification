import numpy as np
from verification_tools import calc_limits

configs = [{'filter':'f277w','idt':200.0},
           {'filter':'f380m','idt':200.0},
           {'filter':'f430m','idt':200.0},
           {'filter':'f480m','idt':400.0}
       ]

idt_fluxes = np.array([config['idt'] for config in configs])*1e-6
apertures = []
apertures = np.array([2.5,2.5,2.5,2.5])*0.0656

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
            'target_xy': [0.0, 0.0],
            'background_subtraction': False,
            "units": "arcsec"
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=100,skyfacs=3.,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/niriss_ami_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/niriss_ami_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
