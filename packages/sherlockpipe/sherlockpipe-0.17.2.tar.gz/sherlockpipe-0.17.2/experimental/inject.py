#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

#::: modules
import numpy as np
import os, sys
import ellc
import transitleastsquares as tls
from transitleastsquares import catalog_info
from transitleastsquares import transit_mask
import astropy.constants as ac
import astropy.units as u
import lightkurve as lk
import pandas as pd


def mask_transits(time, flux, flux_err, periods, radius, rstar_min, rstar_max, mass, mstar_max, mstar_min):
    masks = []
    masked_time = time
    masked_flux = flux
    masked_flux_err = flux_err
    time0 = time
    flux0 = flux
    for period in periods:
        model = tls.transitleastsquares(time0, flux0)
        results = model.power(M_star=mass, M_star_max=mstar_max, M_star_min=mstar_min, R_star=radius,
                              R_star_min=rstar_min, R_star_max=rstar_max,
                              period_min=period - 0.2, period_max=period + 0.2)
        print("Masking transit with period " + str(results.period))
        mask_iteration = transit_mask(time0, results.period, results.duration, results.T0)
        time0 = time[~mask_iteration]
        flux0 = flux[~mask_iteration]
        masks.append(transit_mask(time, results.period, results.duration, results.T0))
    for mask in masks:
        masked_time = masked_time[~mask]
        masked_flux = masked_flux[~mask]
        masked_flux_err = masked_flux_err[~mask]
    return masked_time, masked_flux, masked_flux_err


#::: make model
def make_model(time, flux, flux_err, epoch, period, rplanet, mstar, rstar):
    #a = (7.495e-6 * period**2)**(1./3.)*u.au #in AU
    period_norm = period * u.day
    a = np.cbrt((ac.G * mstar * period_norm ** 2) / (4 * np.pi ** 2)).to(u.au)
    #print("radius_1 =", rstar.to(u.au) / a) #star radius convert from AU to in units of a
    #print("radius_2 =", rplanet.to(u.au) / a)
    texpo = 2./60./24.
    #print("T_expo = ", texpo,"dy")
    #tdur=t14(R_s=radius, M_s=mass,P=period,small_planet=False) #we define the typical duration of a small planet in this star
    #print("transit_duration= ", tdur*24*60,"min" )
    model = ellc.lc(
           t_obs = time,
           radius_1 = rstar.to(u.au) / a, #star radius convert from AU to in units of a
           radius_2 = rplanet.to(u.au) / a, #convert from Rearth (equatorial) into AU and then into units of a
           sbratio = 0,
           incl = 90,
           light_3 = 0,
           t_zero = epoch,
           period = period,
           a = None,
           q = 1e-6,
           f_c = None, f_s = None,
           ldc_1=[0.2755,0.5493], ldc_2 = None,
           gdc_1 = None, gdc_2 = None,
           didt = None,
           domdt = None,
           rotfac_1 = 1, rotfac_2 = 1,
           hf_1 = 1.5, hf_2 = 1.5,
           bfac_1 = None, bfac_2 = None,
           heat_1 = None, heat_2 = None,
           lambda_1 = None, lambda_2 = None,
           vsini_1 = None, vsini_2 = None,
           t_exp=texpo, n_int=None,
           grid_1='default', grid_2='default',
           ld_1='quad', ld_2=None,
           shape_1='sphere', shape_2='sphere',
           spots_1=None, spots_2=None,
           exact_grav=False, verbose=1)

    flux_t = flux + model - 1.
    if model[0] > 0:
        result_flux = flux_t
        flux_err_model = flux_err
        time_custom = time
    else:
        result_flux = []
        time_custom = []
        flux_err_model = []
    return time_custom, result_flux, flux_err_model


def inject(tic, dir, period_grid, phases, radius_grid, periods_to_mask):
    np.random.seed(42)
    lcf = lk.search_lightcurvefile('TIC ' + str(tic), mission="tess", sector=2).download_all()
    ab, mass, massmin, massmax, radius, radiusmin, radiusmax = catalog_info(TIC_ID=tic)
    # units for ellc
    rstar = radius * u.R_sun
    mstar = mass * u.M_sun
    mstar_min = mass - massmin
    mstar_max = mass + massmax
    rstar_min = radius - radiusmin
    rstar_max = radius + radiusmax
    print('\n STELLAR PROPERTIES FOR THE SIGNAL SEARCH')
    print('================================================\n')
    print('limb-darkening estimates using quadratic LD (a,b)=', ab)
    print('mass =', format(mstar, '0.5f'))
    print('mass_min =', format(mstar_min, '0.5f'))
    print('mass_max =', format(mstar_max, '0.5f'))
    print('radius =', format(rstar, '0.5f'))
    print('radius_min =', format(rstar_min, '0.5f'))
    print('radius_max =', format(rstar_max, '0.5f'))
    lc = lcf.PDCSAP_FLUX.stitch().remove_nans()  # remove of the nans
    lc_new = lk.LightCurve(time=lc.time, flux=lc.flux, flux_err=lc.flux_err)
    clean = lc_new.remove_outliers(sigma_lower=float('inf'), sigma_upper=3)  # remove outliers over 3sigma
    flux = clean.flux
    time = clean.time
    flux_err = clean.flux_err
    masked_time, masked_flux, masked_flux_err = mask_transits(time, flux, flux_err, periods_to_mask, radius, rstar_min, rstar_max, mass, mstar_max, mstar_min)
    if not os.path.isdir(dir):
        os.mkdir(dir)
    for period in period_grid:
        for t0 in np.arange(masked_time[60], masked_time[60] + period - 0.1, period / phases):
            for rplanet in radius_grid:
                rplanet = np.around(rplanet, decimals=2) * u.R_earth
                print('\n')
                print('P = ' + str(period) + ' days, Rp = ' + str(rplanet) + ", T0 = " + str(t0))
                time_model, flux_model, flux_err_model = make_model(masked_time, masked_flux, masked_flux_err, t0,
                                                                    period, rplanet, mstar, rstar)
                file_name = os.path.join(dir + '/P' + str(period) + '_R' + str(rplanet.value) + '_' + str(t0) + '.csv')
                lc_df = pd.DataFrame(columns=['#time', 'flux', 'flux_err'])
                lc_df['#time'] = time_model
                lc_df['flux'] = flux_model
                lc_df['flux_err'] = flux_err_model
                lc_df.to_csv(file_name, index=False)


period_grid = np.arange(0.5, 12, 0.5)
phases = 5
radius_grid = np.arange(4, 0.65, -0.1)
periods_to_mask = [4.15]
dir = "curves"
inject(9725627, dir, period_grid, phases, radius_grid, periods_to_mask)
