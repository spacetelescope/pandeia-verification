import numpy as np
from verification_tools import calc_limits
#from verification_tools import fudge_throughput as ft

configs = [{'aperture':'spectroscopy', 'filter':None, 'disperser':'g150', 'bounds':(1.0,1.93)},
           {'aperture':'spectroscopy', 'filter':None, 'disperser':'p120', 'bounds':(0.76,1.8)}]

apertures = np.array([5,5,5,5,5,5,5,5,5,5,5,5])*0.11
idt_fluxes = np.array([1e-2, 1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2])
skyfacs = [2,2,2,2,2,2,2,2,2,2,2,2]
obsmode = {
           'instrument': 'wfi',
           'mode': 'spectroscopy',
           'filter': None,
           'aperture': 'spectroscopy',
           'disperser': 'g150'
           }
exp_config = {
              'subarray': 'spectroscopy',
              'ma_table_name': 'c3b_spec_hlss',
              'nresultants': -1,
              'nexp': 26
              }
strategy = {
            'target_xy': [0.0, 0.0],
            'method': 'specapphot',
            'aperture_size': 0.15,
            'sky_annulus': [0.16,0.5],
            'background_subtraction': False,
            "units": "arcsec"
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=50,skyfacs=skyfacs,
                                 exp_config=exp_config,strategy=strategy,background='roman_minzodi')

np.savez('../../outputs/wfi_spectroscopy_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/wfi_spectroscopy_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
