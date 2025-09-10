import numpy as np
from verification_tools import calc_limits


#configs = [{'filter':'clear','disperser':'prism'},
#           {'filter':'f290lp','disperser':'g395m'}]

configs = [{'filter':'f070lp','disperser':'g140h'},
           {'filter':'f100lp','disperser':'g140h'},
           {'filter':'f170lp','disperser':'g235h'},
           {'filter':'f290lp','disperser':'g395h'},
           {'filter':'f070lp','disperser':'g140m'},
           {'filter':'f100lp','disperser':'g140m'},
           {'filter':'f170lp','disperser':'g235m'},
           {'filter':'f290lp','disperser':'g395m'},
           {'filter':'clear','disperser':'prism'}]

#apertures = np.array([0.21,0.21])
#idt_fluxes = np.array([1e-4,1e-3])
apertures = np.array([0.21,0.21,0.21,0.21,0.21,0.21,0.21,0.21,0.21])
idt_fluxes = np.array([1e-2,1e-2,1e-2,1e-2,1e-3,1e-3,1e-3,1e-3,1e-4])


obsmode = {
           'instrument': 'nirspec',
           'mode': 'mos',
           'filter': 'f070lp',
           'aperture': 'shutter',
           'disperser': 'g140h',
           'slitlet_shape': "slit1x5b2",
           'shutter_location': 'q3_183_86',
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'nrsirs2',
              'ngroup': 14,
              'nint': 1,
              'nexp': 10
              }
strategy = {
            'background_subtraction': True,
            'method': 'msafullapphot',
            'target_xy': [0.0, 0.0],
            'dithers': [
                        {'x':0.0,
                         'y':0.0,
                         'on_source': [False,True,False]}
                       ],
            'shutter_offset': [
                0.0,
                0.0
            ],
            "units": "arcsec"
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=150,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/nirspec_msa_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/nirspec_msa_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])

