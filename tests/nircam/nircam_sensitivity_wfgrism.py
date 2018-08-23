import numpy as np
import astropy.io.fits as fits
from verification_tools import calc_limits
from verification_tools import fudge_throughput as ft

configs = [{'aperture':'lw','filter':'f250m','disperser':'grismr','bounds':(2.421,2.581)},
           {'aperture':'lw','filter':'f277w','disperser':'grismr','bounds':(2.421,3.09)},
           {'aperture':'lw','filter':'f300m','disperser':'grismr','bounds':(2.848,3.137)},
           {'aperture':'lw','filter':'f322w2','disperser':'grismr','bounds':(2.451,3.958)},
           {'aperture':'lw','filter':'f335m','disperser':'grismr','bounds':(3.207,3.502)},
           {'aperture':'lw','filter':'f356w','disperser':'grismr','bounds':(3.152,3.942)},
           {'aperture':'lw','filter':'f360m','disperser':'grismr','bounds':(3.442,3.777)},
           {'aperture':'lw','filter':'f410m','disperser':'grismr','bounds':(3.914,4.257)},
           {'aperture':'lw','filter':'f430m','disperser':'grismr','bounds':(4.195,4.367)},
           {'aperture':'lw','filter':'f444w','disperser':'grismr','bounds':(3.929,4.949)},
           {'aperture':'lw','filter':'f460m','disperser':'grismr','bounds':(4.543,4.713)},
           {'aperture':'lw','filter':'f480m','disperser':'grismr','bounds':(4.693,4.921)}]
     
apertures = np.array([2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5])*0.0648
idt_fluxes = np.array([1e-2, 1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2,1e-2])
skyfacs = [2,2,2,2,2,2,2,2,2,2,2,2]
obsmode = {
           'instrument': 'nircam',
           'mode': 'wfgrism',
           'filter': 'f090w',
           'aperture': 'lw',
           'disperser': 'grismr'
           }
exp_config = {
              'subarray': 'full',
              'readmode': 'deep8',
              'ngroup': 5,
              'nint': 1,
              'nexp': 10
              }
strategy = {
            'method': 'specapphot',
            'aperture_size': 0.15,
            'sky_annulus': [0.16,0.5],
            'background_subtraction': False
            }
    
output = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=5,skyfacs=skyfacs,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/nircam_wfgrism_sensitivity.npz',
    wavelengths=output['wavelengths'], sns=output['sns'], lim_fluxes=output['lim_fluxes'], sat_limits=output['sat_limits'], configs=output['configs'])
