import numpy as np
from verification_tools import calc_limits

configs = [{'filter':'f090w','idt':14.46},
           {'filter':'f115w','idt':12.13},
           {'filter':'f140m','idt':18.88},
           {'filter':'f150w','idt':11.27},
           {'filter':'f158m','idt':10.67},
           {'filter':'f200w','idt':9.12},
           {'filter':'f277w','idt':7.66},
           {'filter':'f356w','idt':7.94},
           {'filter':'f380m','idt':24.89},
           {'filter':'f430m','idt':33.73},
           {'filter':'f444w','idt':13.18},
           {'filter':'f480m','idt':41.31}
       ]

idt_fluxes = np.array([config['idt'] for config in configs])*1e-6
wave_centers = np.array([0.9,1.15,1.40,1.50,1.58,2.00,2.77,3.56,3.80,4.30,4.44,4.80])
apertures = np.array([1.54,1.54,1.54,1.54,1.54,1.54,2.5,2.5,2.5,2.72,2.72,2.72])*0.0646

obsmode = {
           'instrument': 'niriss',
           'mode': 'imaging',
           'filter': 'f090w',
           'aperture': 'imager',
           'disperser': None
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'nisrapid',
              'ngroup': 93,
              'nint': 1,
              'nexp': 10
              }
strategy = {
            'method': 'imagingapphot',
            'aperture_size': 0.1,
            'sky_annulus': [1,3],
            'target': [0.0, 0.0],
            'background_subtraction': False
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=50,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')


np.savez('../../outputs/niriss_imaging_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/niriss_imaging_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
