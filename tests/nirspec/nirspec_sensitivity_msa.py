import numpy as np
import astropy.io.fits as fits
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
           'mode': 'msa',
           'filter': 'f070lp',
           'aperture': 'shutter',
           'disperser': 'g140h',
           'slitlet_shape': [[0,-2],[0,0],[0,2]]
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'nrsirs2',
              'ngroup': 14,
              'nint': 1,
              'nexp': 10
              }
strategy = {
            'method': 'msafullapphot',
            'dithers': [
                        {'x':0.0,
                         'y':0.0,
                         'on_source': [False,True,False]}
                       ]
            }

output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=150,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/nirspec_msa_sensitivity.npz',
    wavelengths=output[0]['wavelengths'], sns=output[0]['sns'], lim_fluxes=output[0]['lim_fluxes'], sat_limits=output[0]['sat_limits'], configs=output[0]['configs'])

np.savez('../../outputs/nirspec_msa_sensitivity_one.npz',
    wavelengths=output[1]['wavelengths'], sns=output[1]['sns'], lim_fluxes=output[1]['lim_fluxes'], sat_limits=output[1]['sat_limits'], configs=output[1]['configs'])

