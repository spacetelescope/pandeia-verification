from __future__ import print_function

import os
import numpy as np
import scipy.interpolate as ip
#import matplotlib.pylab as plt
import scipy.constants as con
from astropy.io import fits, ascii

from pandeia.engine.perform_calculation import perform_calculation

def calc_limits(configs, apertures, fluxes, scanfac=10, obsmode=None,
                exp_config=None, exp_configs=None, strategy=None, nflx=40,
                background='miri',skyfacs=None,orders=None,lim_snr=10.0):

    """
    Script to calculate sensitivity limits for extended sources using Pandeia. The script calculates a
    grid of models by varying the source flux density, yielding a numerical function SNR(F).
    The sensitivity limit is then calculated by inverting the function SNR(F) => F(SNR=lim_snr). It is possible
    to calculate the limiting sensitivity for a single Pandeia configuration, or for a list of N configurations,
    with some limitations. Most often, the user will probably loop over a list of N configurations, varying a filter,
    grating or other parameter.

    Parameters
    ----------
    configs: list of N dicts
        Contains dictionaries containing keyword/value pairs relevant for a Pandeia obsmode.
        For a given mode, passed values will be replaced, while others will default. These are the values
        of the configuration that are VARIED. For instance, the user might want to loop over different filter values.
    apertures: list of N floats
        Extraction apertures for each config.
    fluxes: List of N floats
        Initial guess of limiting flux in mJy
    scanfac: float
        Factor within which to search for the limiting flux. IMPORTANT: It is currently the users
        responsibility to check that the limiting flux is contained within fluxes/scanfac -> fluxes*scanfac.
        for spectroscopic modes, this should be true for every wavelength.
    obsmode: dict
        These are dictionary keyword/value pairs of a Pandeia obsmode that are NOT varied. Typically,
        this would identify the instrument and mode.
    exp_config: dict
        This is a dictionary of non-default values for a Pandeia exposure configuration.
        Set EITHER exp_config OR exp_configs.
    exp_configs: list of N dicts
        The user may want to use a different set of exposure configs for every obsmode config.
        In that case use this to pass N different versions.
    strategy: dict
        A dictionary containing a valid Pandeia strategy. It is currently not possible to change the
        strategy for every configuration.
    nflx: Integer
        Number of flux values in the grid. 10 is a reasonable default if the limit guess is close.
    background: String
        Invoke a canned background. There are various option, but most people will want to set this to "minzodi12".
        It is currently not possible to pass a new background beyond editing this scripts, but but it would not be
        difficult to implement.
    skyfacs: float
        If the strategy is set to use background subtraction, this sets the size of the sky extraction aperture relative to the
        extraction aperture.
    orders: List of N integers
        This sets the order for each configuration. This is the only strategy parameter that can currently be varied.
    lim_snr: float
        Limiting signal-to-noise ratio. The standard (and default) is 10.0.


    Returns
    ----------
    Dictionary containing:
        configs: List of the input Pandeia configurations
        strategy:  List of the input Pandeia strategies
        wavelengths: The effective wavelength for imaging modes and wavelength arrays for spectroscopic modes
        sns: The signal-to-noise ratio for each configuration. This is for debugging purposes.
        lim_fluxes: The calculated limiting flux densities in mJy/extraction aperture size.
        source_rates_per_njy: Detected electron rates for a source of 1 nJy.
        sat_limits: The calculated saturation limit
        orders: The input spectral order
        line_limits: Limiting integrated line flux in W/m^2/extraction aperture size.

    """

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
    elif background in ['nircam_061416']:
        syspath = os.path.abspath(os.path.dirname(__file__))
        bg_table = ascii.read(os.path.join(syspath,'inputs/nircam_verification_background_mrieke_061416.tab'))
        wave_mu = bg_table['col1'].data
        flambda = bg_table['col2'].data
        scat_MJy = bg_table['col3'].data
        c_mu = con.c*1e6
        fnu = (wave_mu**2/c_mu)*flambda
        fnu_Jy = fnu*1e26
        fnu_MJy = fnu_Jy/1e6
        background = [wave_mu,fnu_MJy+scat_MJy]
    elif background in ['niriss']:
        syspath = os.path.abspath(os.path.dirname(__file__))
        bg_table = ascii.read(os.path.join(syspath,'inputs/NIRISS_background.txt'))
        background = [bg_table['col1'].data,bg_table['col2'].data]
    elif background in ['zodi_only']:
        syspath = os.path.abspath(os.path.dirname(__file__))
        bg_table = ascii.read(os.path.join(syspath,'inputs/zodi_standard.txt'))
        background = [bg_table['col1'].data,bg_table['col2'].data]
    elif background in ['minzodi12']:
        syspath = os.path.abspath(os.path.dirname(__file__))
        bg_table = fits.getdata(os.path.join(syspath,'inputs/minzodi12_12052016.fits'))
        background = [bg_table['wavelength'],bg_table['background']]


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
            'geometry': 'flat',
            'norm_method': 'surf_center',
            'surf_area_units': 'arcsec^2',
            'major': 0.9,
            'minor': 0.9
        },
        'spectrum': {
            'normalization': {
                'type': 'at_lambda',
                'norm_waveunit': 'microns',
                'norm_fluxunit': 'mjy',
                'norm_flux': 0.1,
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

    wavelengths = []
    sns = []
    lim_fluxes = []
    sat_limits = []
    line_limits = []
    source_rates = []
    for i in range(len(configs)):
        config = configs[i]
        aperture = apertures[i]
        flux = fluxes[i]

        if np.size(exp_configs)>1:
            exp_config = exp_configs[i]

        if np.size(skyfacs)>1:
            skyfac = skyfacs[i]
        else:
            skyfac = skyfacs

        strategy['aperture_size'] = aperture
        if orders is not None:
            strategy['order'] = orders[i]

        if skyfacs is None:
            inner_fac = 2.
            outer_fac = 5.
        else:
            if obsmode['mode'] in ['msa','fixed_slit','lrsslit','lrsslitless','wfgrism','ssgrism','wfss','soss']:
                inner_fac = 1.5
                outer_fac = inner_fac+skyfac/2.
            elif obsmode['mode'] in ['ifu','mrs','sw_imaging','lw_imaging','imaging','ami']:
                inner_fac = 2.
                outer_fac = np.sqrt(skyfac+inner_fac**2.)

        if 'sky_annulus' in strategy.keys():
            strategy['sky_annulus'] = [aperture*inner_fac,aperture*outer_fac]

        for key in config.keys():
            obsmode[key] = config[key]

        scene = [source]

        flx_expansion = np.logspace(np.log10(flux/scanfac),np.log10(flux*scanfac),nflx)

        sn_arr = []

        for flux in flx_expansion:

            source['spectrum']['normalization']['norm_flux'] = flux

            input = {
                'scene': scene,
                'background': background,
                'configuration': {'instrument': obsmode,
                'detector': exp_config},
                'strategy': strategy
            }

            report = perform_calculation(input, dict_report=False)
            bg_pix_rate = np.min(report.bg_pix)
            aperture_source_rate = report.curves['extracted_flux'][1]
            aperture_bg_rate = report.curves['extracted_flux_plus_bg'][1][0]-aperture_source_rate[0]
            fov_source_rate = report.curves['total_flux'][1]
            fits_dict = report.as_fits()

            sn_arr.append(fits_dict['1d']['sn'][0].data['sn'])

            wavelength = fits_dict['1d']['sn'][0].data['wavelength']

        bsubs = np.isinf(fits_dict['1d']['sn'][0].data['sn'])

        sn_arr = np.array(sn_arr)
        lim_flx = np.array([np.interp(lim_snr,sn_arr[:,i],flx_expansion) for i in np.arange(wavelength.size)])
        # Make sure that undefined points remain undefined in the limiting flux
        lim_flx[bsubs] = np.nan

        if len(lim_flx)>0:
            lim_flx = lim_flx.flatten()

        wavelengths.append(wavelength)
        sns.append(fits_dict['1d']['sn'][0].data['sn'])
        lim_fluxes.append(lim_flx)
        source_rates.append(aperture_source_rate/flux/1e6)

        nwaves = np.size(aperture_source_rate)

        midpoint = int(nwaves/2)

        #The best one at the midpoint. It doesn't really matter what the reference spectrum is here. We
        #just need one to calculate the rate per mJy for the saturation estimate.
        source['spectrum']['normalization']['norm_flux'] = lim_flx[midpoint]

        input = {
            'scene': [source],
            'background': background,
            'configuration': {'instrument': obsmode,
            'detector': exp_config},
            'strategy': strategy
        }

        report = perform_calculation(input, dict_report=False)
        fits_dict = report.as_fits()
        res_dict = report.as_dict()

        aperture_source_rate = report.curves['extracted_flux'][1]
        aperture_total_rate = report.curves['extracted_flux_plus_bg'][1]
        aperture_bg_rate = aperture_total_rate-aperture_source_rate
        fov_source_rate = report.curves['total_flux'][1]

        tgroup = report.signal.current_instrument.the_detector.exposure_spec.tgroup
        tframe =  report.signal.current_instrument.the_detector.exposure_spec.tframe
        tfffr = report.signal.current_instrument.the_detector.exposure_spec.tfffr
        #det_type = report.signal.current_instrument.the_detector.exposure_spec.det_type

        #nprerej =  report.signal.current_instrument.the_detector.exposure_spec.nprerej

        if obsmode['instrument'] != 'miri':
            mintime = 2 * tframe
        else:
            mintime = 5 * tframe #minimum recommended frames is 5 for MIRI

        # Soss is rotated by 90 degrees on the detector, for some reason
        if obsmode['mode'] == 'soss':
            report.bg_pix = np.rot90(report.bg_pix)
            report.signal.rate = np.rot90(report.signal.rate)

        # Spectrum?
        if (lim_flx.shape[0]>1) and (report.signal.rate.shape[1]!=lim_flx.shape[0]):
            #slitless modes have excess pixels on each side - excess should always be an odd integer
            excess = (report.signal.rate.shape[1]-lim_flx.shape[0])-1
        else:
            excess=0

        if excess==0:
            fullwell_minus_bg = (report.signal.the_detector.fullwell-mintime*report.bg_pix)
            rate_per_mjy = report.signal.rate/lim_flx[midpoint]
            bg_pix_rate_min = np.min(report.bg_pix,0)
            bg_pix_rate_max = np.max(report.bg_pix,0)
        else:
            bg_pix_rate_min = np.min(report.bg_pix[:,int(excess/2):-int(excess/2)])
            bg_pix_rate_max = np.max(report.bg_pix[:,int(excess/2):-int(excess/2)])
            fullwell_minus_bg = (report.signal.the_detector.fullwell-mintime*report.bg_pix[:,int(excess/2):-int(excess/2)-1])
            rate_per_mjy = report.signal.rate[:,int(excess/2):-int(excess/2)-1]/lim_flx[midpoint]

        sat_limit_detector = fullwell_minus_bg/mintime/np.abs(rate_per_mjy) #units of mJy

        # Calculate line sensitivities, assuming unresolved lines.
        if lim_flx.shape[0]>1:
            sat_limit = np.min(sat_limit_detector,0)
            r = report.signal.current_instrument.get_resolving_power(wavelength)
            px_width_micron = np.abs(wavelength-np.roll(wavelength,1))
            px_width_micron[:1] = px_width_micron[1]

            freqs = 2.99792458e14/wavelength
            px_width_hz = np.abs(freqs-np.roll(freqs,1))
            px_width_hz[:1] = px_width_hz[1]

            line_width_px = wavelength/r/px_width_micron
            line_limit = lim_flx*1e-3*1e-26 * px_width_hz * line_width_px / np.sqrt(line_width_px)
            line_limits.append(line_limit)
        else:
            sat_limit = np.min(sat_limit_detector)

        sat_limits.append(sat_limit)

        print('Configuration:', config)
        print('Exposure Time:', '{:7.2f}'.format(res_dict['scalar']['exposure_time']))
        print('Total Exposure Time:', '{:7.2f}'.format(res_dict['scalar']['total_exposure_time']))
        print('Extracted flux/nJy:', aperture_source_rate[midpoint]/lim_flx[midpoint]/1e6)
        print('Saturation limit [mJy]', '{:7.2f}'.format(np.min(sat_limit)))
        print('Extracted source in e-/s:', '{:7.2f}'.format(aperture_source_rate[midpoint]))
        print('Extracted flux plus background in e-/s:', '{:7.2f}'.format(aperture_total_rate[midpoint]))
        print('Encircled energy:', '{:7.2f}'.format(100*aperture_source_rate[midpoint]/fov_source_rate[int(fov_source_rate.shape[0]/2)])+'%')
        print('Background rate per pix (min and max):', '{:7.2f}'.format(np.min(bg_pix_rate_min)), '{:7.2f}'.format(np.max(bg_pix_rate_max)))
        print('Aperture radius:', aperture, 'arcseconds')
        print('Extraction area [sq. pixels]:', report.extraction_area)
        print('Background area [sq. pixels]:', report.background_area )
        print('Limiting flux:', '{:7.2e}'.format(np.min(lim_flx)),'mJy')
        print('SNR:', '{:7.2f}'.format(fits_dict['1d']['sn'][0].data['sn'][midpoint]))
        print('Reference wavelength:', '{:7.2e}'.format(fits_dict['1d']['sn'][0].data['wavelength'][midpoint]))

    return {'configs':configs,'strategy':strategy, 'wavelengths':wavelengths,'sns':sns,'lim_fluxes':lim_fluxes,
            'source_rates_per_njy':source_rates, 'sat_limits':sat_limits, 'orders':orders, 'line_limits':line_limits}
