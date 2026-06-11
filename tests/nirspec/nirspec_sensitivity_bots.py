import copy

import numpy as np
from verification_tools import calc_limits
from pandeia.engine.data_util import InstrumentConfiguration

configs = []
idt_fluxes = []
instrument = InstrumentConfiguration("jwst", "nirspec", webapp=True)
instrument.set_mode("bots")
instrument.set_aperture("s1600a1")
for sub in instrument.subarrays:
    new_instrument = copy.deepcopy(instrument)
    new_instrument.set_element("subarray", sub)
    for disp in new_instrument.dispersers:
        new_instrument.set_element("disperser", disp)
        for filt in new_instrument.filters:
            configs.append({"subarray": sub, "filter": filt, "disperser": disp})
            if "prism" in disp:
                idt_fluxes.append(1e-4)
            elif "m" in disp:
                idt_fluxes.append(1e-3)
            elif "h" in disp:
                idt_fluxes.append(1e-2)

apertures = np.array([0.42] * len(configs))
idt_fluxes = np.array(idt_fluxes)
skyfacs = np.array([2.0] * len(configs))


#apertures = np.array([0.1*7.6,0.1*2,0.1*2])
#idt_fluxes = np.array([2e-4, 1e-4,1e-4])
#skyfacs = np.array([1., 4.,2.])

obsmode = {
           'instrument': 'nirspec',
           'mode': 'bots',
           'filter': 'f070lp',
           'aperture': 's1600a1',
           'disperser': 'g140h'
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'nrsirs2',
              'ngroup': 14,
              'nint': 1,
              'nexp': 10
              }
strategy = {
            'method': 'specapphot',
            'aperture_size': 0.15,
            'sky_annulus': [0.16,0.5],
            'target_xy': [0.0, 0.0],
            'dithers': [{'x':0.0,'y':0.0}],
            'background_subtraction': True,
            "units": "arcsec"
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=150,skyfacs=skyfacs,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/nirspec_bots_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/nirspec_bots_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
