import numpy as np
from verification_tools import calc_limits

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

apertures = np.array([5,5,5,5,5,5,5,5,5,5,5,5])*0.0648
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
              'readout_pattern': 'deep8',
              'ngroup': 5,
              'nint': 1,
              'nexp': 10
              }
strategy = {
            'method': 'specapphot',
            'aperture_size': 0.15,
            'sky_annulus': [0.16,0.5],
            'background_subtraction': False,
            'target_xy': [0.0, 0.0]
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=10000000,skyfacs=skyfacs,nflx=80,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/nircam_wfgrism_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/nircam_wfgrism_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
