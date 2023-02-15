import os
import numpy as np
import scipy.interpolate as ip
import matplotlib.pylab as plt
from astropy.io import fits, ascii

from pandeia.engine.perform_calculation import perform_calculation

def calc_backgrounds(configs, obsmode=None, 
                     exp_config=None, strategy=None, background='miri'):

    if background == 'miri':
        syspath = os.path.abspath(os.path.dirname(__file__))
        bg_table = ascii.read(os.path.join(syspath,'inputs/miri_verification_background.tab'))
        # From the matlab doc, it appears that the thermal background is not subjected to the OTE transmission
        background = [bg_table['col1'].data,bg_table['col2'].data]
    elif background in ['nirspec']:
        syspath = os.path.abspath(os.path.dirname(__file__))
        bg_table = fits.getdata(os.path.join(syspath,'inputs/nirspec_verification_background.fits'))
        background = [bg_table['wavelength'],bg_table['intensity']]
    elif background in ['nircam']:
        syspath = os.path.abspath(os.path.dirname(__file__))
        bg_table = ascii.read(os.path.join(syspath,'inputs/nircam_verification_background.tab'))
        background = [bg_table['col1'].data,bg_table['col2'].data]
    elif background in ['niriss']:
        syspath = os.path.abspath(os.path.dirname(__file__))
        bg_table = ascii.read(os.path.join(syspath,'inputs/nircam_verification_background.tab'))
        background = [bg_table['col1'].data,bg_table['col2'].data]
    
    source = {
        'id': 1,
        'target': True,
        'position': {
            'orientation': 23.0,
            'ang_unit': 'arcsec',
            'x_offset': 0.0,
            'y_offset': 0.0,
        },
        'shape': {
            'major': 0.0,
            'minor': 0.0
        },
        'spectrum': {
            'normalization': {
                'type': 'at_lambda',
                'norm_waveunit': 'microns',
                'norm_fluxunit': 'mjy',
                'norm_flux': 1e-10,
                'norm_wave': 2.},
                'sed': {
                    'sed_type': 'input',
                    'wmin': 0.4,
                    'wmax': 30.,
                    'sed_type': 'flat',
                },
                'lines': []
            }
        }

    bgs = []
    wavelengths = []
    for config in configs:
        
        for key in config.keys():
            obsmode[key] = config[key] 

        scene = [source]
    
        calc_input = {
            'scene': scene,
            'background': background,
            'configuration': {'instrument': obsmode,
            'detector': exp_config},
            'strategy': strategy
        }  
    
        report = perform_calculation(calc_input, dict_report=False)

        if report.bg_pix.shape[0] != report.bg_pix.shape[1]:
            bg_pix_rate = np.max(report.bg_pix,axis=0)
        else:
            bg_pix_rate = np.max(report.bg_pix)
        
        fits_dict = report.as_fits()
       
        wavelength = fits_dict['1d']['sn'][0].data['wavelength']
        
        print('configuration:', config)

        bgs.append(bg_pix_rate)
        wavelengths.append(wavelength)
    
    return {'wavelengths':wavelengths,'backgrounds':bgs,'configs':configs}
