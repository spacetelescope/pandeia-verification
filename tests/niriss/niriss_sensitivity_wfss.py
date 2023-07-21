import numpy as np
from verification_tools import calc_limits

configs = [{'aperture':'imager','filter':'f090w','disperser':'gr150r','bounds':(0.8,0.989)},
           {'aperture':'imager','filter':'f115w','disperser':'gr150r','bounds':(1.021,1.268)},
           {'aperture':'imager','filter':'f140m','disperser':'gr150r','bounds':(1.346,1.465)},
           {'aperture':'imager','filter':'f150w','disperser':'gr150r','bounds':(1.346,1.653)},
           {'aperture':'imager','filter':'f158m','disperser':'gr150r','bounds':(1.506,1.667)},
           {'aperture':'imager','filter':'f200w','disperser':'gr150r','bounds':(1.772,2.207)}]

apertures = np.array([3,3,3,3,3,3])*0.0656
idt_fluxes = np.array([2e-4, 2e-4,2e-4,2e-4,2e-4,2e-4])
skyfacs = [2,2,2,2,2,2]
obsmode = {
           'instrument': 'niriss',
           'mode': 'wfss',
           'filter': 'f090w',
           'aperture': 'imager',
           'disperser': 'gr150r'
           }
exp_config = {
              'subarray': 'full',
              'readout_pattern': 'nis',
              'ngroup': 23,
              'nint': 1,
              'nexp': 10
              }
strategy = {
            'target_xy': [0.0, 0.0],
            'method': 'specapphot',
            'aperture_size': 0.1,
            'sky_annulus': [0.16,0.5],
            'background_subtraction': False,
            "units": "arcsec"
            }

outputs_regular, outputs_one = calc_limits.calc_limits(configs,apertures,idt_fluxes,obsmode=obsmode,scanfac=500,skyfacs=skyfacs,
                                 exp_config=exp_config,strategy=strategy,background='minzodi12')

np.savez('../../outputs/niriss_wfss_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/niriss_wfss_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
