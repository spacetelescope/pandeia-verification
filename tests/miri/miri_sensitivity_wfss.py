import numpy as np
from verification_tools import calc_limits

configs = [{'aperture':'imager','mode':'wfss'}]
apertures = np.array([0.84])*7.5/10.
idt_fluxes = np.array([5e-3])

obsmode = {
           'instrument': 'miri',
           'mode': 'wfss',
           'filter': None,
           'aperture': 'imager',
           'disperser': 'p750l'
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'fastr1',
              'ngroup': 180,
              'nint': 1,
              'nexp': 20
              }
strategy = {
            'target_xy': [0.0, 0.0],
            'method': 'specapphot',
            'aperture_size': 1.1,
            'sky_annulus': [1.11,3.2],
            'background_subtraction': False,
            "units": "arcsec"
            }


outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=1000,nflx=80,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/miri_wfss_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'],
    source_rates_per_njy=outputs_regular['source_rates_per_njy'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'], line_limits=outputs_regular['line_limits'])

np.savez('../../outputs/miri_wfss_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'],
    source_rates_per_njy=outputs_one['source_rates_per_njy'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'], line_limits=outputs_one['line_limits'])
