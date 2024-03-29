import numpy as np
from verification_tools import calc_limits

configs = [{'filter':'f250m','idt':28.33},
           {'filter':'f277w','idt':12.70},
           {'filter':'f300m','idt':22.94},
           {'filter':'f322w2','idt':8.55},
           {'filter':'f323n','idt':166.61},
           {'filter':'f335m','idt':19.43},
           {'filter':'f356w','idt':12.83},
           {'filter':'f360m','idt':20.37},
           {'filter':'f405n','idt':173.92},
           {'filter':'f410m','idt':22.00},
           {'filter':'f430m','idt':46.66},
           {'filter':'f444w','idt':20.63},
           {'filter':'f460m','idt':73.56},
           {'filter':'f466n','idt':235.43},
           {'filter':'f470n','idt':286.00},
           {'filter':'f480m','idt':82.12}
       ]


idt_fluxes = np.array([config['idt'] for config in configs])*1e-6
#wave_centers = np.array([2.5,2.77,3.0,3.22,3.23,3.35,3.56,3.60,4.05,4.10,4.18,4.30,4.44,4.60,4.66,4.70,4.80])
pixscale = 0.0648  # arcsec
#diameter_flat_to_flat = 6.5 * 1e6 # meters to micron
#apertures = []
#for wave_center in wave_centers:
#    apertures.append(np.max([2.5*pixscale, (1.25 * (wave_center / diameter_flat_to_flat) *
#                     (180 * 3600 / np.pi))]))
apertures = np.array([2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.622,2.712,2.839,2.85,2.88,2.939])*pixscale

obsmode = {
           'instrument': 'nircam',
           'mode': 'lw_imaging',
           'filter': 'f250m',
           'aperture': 'lw',
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
            'aperture_size': 0.1,
            'sky_annulus': [0.11,3.2],
            'target_xy': [0.0, 0.0],
            'dithers': [{'x':0.0,'y':0.0}],
            'background_subtraction': False,
            "units": "arcsec"
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=100,skyfacs=2.,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')
np.savez('../../outputs/nircam_lw_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/nircam_lw_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
