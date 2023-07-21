import numpy as np
from verification_tools import calc_limits


#configs = [{'filter':'clear','disperser':'prism'},
#           {'filter':'f100lp','disperser':'g140h'},
#           {'filter':'f170lp','disperser':'g235m'}]
configs = [{'filter':'f070lp','disperser':'g140h'},
           {'filter':'f100lp','disperser':'g140h'},
           {'filter':'f170lp','disperser':'g235h'},
           {'filter':'f290lp','disperser':'g395h'},
           {'filter':'f070lp','disperser':'g140m'},
           {'filter':'f100lp','disperser':'g140m'},
           {'filter':'f170lp','disperser':'g235m'},
           {'filter':'f290lp','disperser':'g395m'},
           {'filter':'clear','disperser':'prism'}]

#apertures = np.array([0.1*1.7,0.1*1.7,0.1*1.7])
#idt_fluxes = np.array([1e-4,5e-3,1e-3])
#skyfacs = np.array([1.,1.,1.])
apertures = np.array([0.105*2,0.105*2,0.105*2,0.105*2,0.105*2,0.105*2,0.105*2,0.105*2,0.105*2])
idt_fluxes = np.array([1e-2,1e-2,1e-2,1e-2,1e-3,1e-3,1e-3,1e-3,1e-4])

obsmode = {
           'instrument': 'nirspec',
           'mode': 'ifu',
           'filter': 'f070lp',
           'aperture': 'ifu',
           'disperser': 'g140h'
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'nrsirs2',
              'ngroup': 17,
              'nint': 1,
              'nexp': 4
              }
strategy = {
            'target_xy': [0.0, 0.0],
            'method': 'ifunodinscene',
            'aperture_size': 0.15,
            'dithers': [{'x':0,'y':0},{'x':1,'y':1}],
            "units": "arcsec"
           }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=150,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/nirspec_ifu_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/nirspec_ifu_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
