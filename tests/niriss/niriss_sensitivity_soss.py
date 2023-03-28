import numpy as np
from verification_tools import calc_limits

configs = [{'aperture':'soss','filter':'clear','disperser':'gr700xd'},
           {'aperture':'soss','filter':'clear','disperser':'gr700xd'}]

apertures = np.array([2.5,2.5])*0.0656
idt_fluxes = np.array([0.03, 0.03])
orders = [1,2]
obsmode = {
           'instrument': 'niriss',
           'mode': 'soss',
           'filter': 'clear',
           'aperture': 'soss',
           'disperser': 'gr700xd'
           }
exp_config = {
              'subarray': 'substrip256',
              'readout_pattern': 'nisrapid',
              'ngroup': 36,
              'nint': 1,
              'nexp': 5
              }
strategy = {
            'method': 'soss',
            'background_subtraction': False,
            'order': 1
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=1000,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12',orders=orders)

np.savez('../../outputs/niriss_soss_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'], orders=outputs_regular['orders'])

np.savez('../../outputs/niriss_soss_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'], orders=outputs_one['orders'])
