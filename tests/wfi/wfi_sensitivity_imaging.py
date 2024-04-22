import numpy as np
from verification_tools import calc_limits
#from verification_tools import fudge_throughput as ft

configs = [{'filter':'f062','idt':70.00},
           {'filter':'f087','idt':120.00},
           {'filter':'f106','idt':120.00},
           {'filter':'f129','idt':120.00},
           {'filter':'f146','idt':70.00},
           {'filter':'f158','idt':120.00},
           {'filter':'f184','idt':200.00},
           {'filter':'f213','idt':200.00}
       ]


idt_fluxes = np.array([config['idt'] for config in configs])*1e-6
#wave_centers = np.array([2.5,2.77,3.0,3.22,3.23,3.35,3.56,3.60,4.05,4.10,4.18,4.30,4.44,4.60,4.66,4.70,4.80])
pixscale = 0.11  # arcsec
#diameter_flat_to_flat = 6.5 * 1e6 # meters to micron
#apertures = []
#for wave_center in wave_centers:
#    apertures.append(np.max([2.5*pixscale, (1.25 * (wave_center / diameter_flat_to_flat) *
#                     (180 * 3600 / np.pi))]))
apertures = np.array([2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5])*pixscale

obsmode = {
           'instrument': 'wfi',
           'mode': 'imaging',
           'filter': 'f062',
           'aperture': 'imaging',
           'disperser': None
           }
exp_config = {
              'subarray': 'imaging',
              'ma_table_name': 'hltds_imaging1',
              'nresultants': -1,
              'nexp': 62
              }
strategy = {
            'method': 'imagingapphot',
            'aperture_size': 0.5,
            'sky_annulus': [0.6,3.2],
            'target_xy': [0.0, 0.0],
            'dithers': [{'x':0.0,'y':0.0}],
            'background_subtraction': False,
            "units": "arcsec"
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=100,skyfacs=2.,
                                 exp_config=exp_config,strategy=strategy,background='roman_minzodi')

np.savez('../../outputs/wfi_imaging_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/wfi_imaging_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
