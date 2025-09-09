import copy
import numpy as np
from verification_tools import calc_limits
#from verification_tools import fudge_throughput as ft

configs = [{'aperture':'spectroscopy', 'filter':None, 'disperser':'grism', 'bounds':(1.0,1.93)},
           {'aperture':'spectroscopy', 'filter':None, 'disperser':'prism', 'bounds':(0.76,1.8)}]

apertures = np.array([5,5,5,5,5,5,5,5,5,5,5,5] * 18)*0.11
detectors = [
            "wfi01",
            "wfi02",
            "wfi03",
            "wfi04",
            "wfi05",
            "wfi06",
            "wfi07",
            "wfi08",
            "wfi09",
            "wfi10",
            "wfi11",
            "wfi12",
            "wfi13",
            "wfi14",
            "wfi15",
            "wfi16",
            "wfi17",
            "wfi18"
            ]
def add_detector(configs):
    out_config = []
    for detector in detectors:
        for config in configs:
            config["detector"] = detector
            out_config.append(copy.deepcopy(config))
    return out_config

configs = add_detector(configs)


idt_fluxes = np.array([2e-2, 2e-2,2e-2,2e-2,2e-2,2e-2,2e-2,2e-2,2e-2,2e-2,2e-2,2e-2] * 18)
skyfacs = [2,2,2,2,2,2,2,2,2,2,2,2] * 18
obsmode = {
           'instrument': 'wfi',
           'mode': 'spectroscopy',
           'filter': None,
           'aperture': 'spectroscopy',
           'disperser': 'grism',
           'detector': 'wfi01'
           }
exp_config = {
              'subarray': 'spectroscopy',
              'ma_table_name': 'sp_300_16',
              'nresultants': -1,
              'nexp': 33
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
                                 exp_config=exp_config,strategy=strategy,background='roman_hlwas')

np.savez('../../outputs/wfi_spectroscopy_sensitivity.npz',
    wavelengths=outputs_regular['wavelengths'], sns=outputs_regular['sns'], lim_fluxes=outputs_regular['lim_fluxes'], sat_limits=outputs_regular['sat_limits'], configs=outputs_regular['configs'])

np.savez('../../outputs/wfi_spectroscopy_sensitivity_one.npz',
    wavelengths=outputs_one['wavelengths'], sns=outputs_one['sns'], lim_fluxes=outputs_one['lim_fluxes'], sat_limits=outputs_one['sat_limits'], configs=outputs_one['configs'])
