from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia as aq_gaia
import astropy.units as u
from uncertainties import ufloat
from collections import namedtuple as nt

width = u.Quantity(0.0005, u.deg)
height = u.Quantity(0.0005, u.deg)

class Gaia:
    def __init__(self,coordinate : SkyCoord):
        query = aq_gaia.query_object_async(coordinate=coordinate, width=width, height=height)

        ra = ufloat(float(query['ra']), float(query['ra_error']))
        dec = ufloat(float(query['dec']), float(query['dec_error']))

        self.id = int(query['solution_id'])

        self.coord = SkyCoord(ra.nominal_value*u.deg
                               ,dec.nominal_value*u.deg
                               )
        self.parallax = ufloat(query['parallax'],query['parallax_error'])
        self.pm = (ufloat(query['pmra'],query['pmra_error']),ufloat(query['pmdec'],query['pmdec_error']))

        self.g = float(query['phot_g_mean_mag'])*u.mag
        self.bp = float(query['phot_bp_mean_mag']) * u.mag
        self.rp = float(query['phot_rp_mean_mag']) * u.mag

        self.bp_rp = float(query['bp_rp']) * u.mag
        self.bp_g = float(query['bp_g']) * u.mag
        self.g_rp = float(query['g_rp']) * u.mag

        self.radial_velocity = ufloat(float(query['radial_velocity']),query['radial_velocity_error'])

        t_err = max(
                abs(float(query['teff_val']) - float(query['teff_percentile_lower'])),
                abs(float(query['teff_val']) - float(query['teff_percentile_upper'])))

        self.t_eff = ufloat(float(query['teff_val']),t_err)

        r_err = max(
            abs(float(query['radius_val']) - float(query['radius_percentile_lower'])),
            abs(float(query['radius_val']) - float(query['radius_percentile_upper'])))

        self.radius = ufloat(float(query['radius_val']),r_err)

        l_err = max(
            abs(float(query['lum_val']) - float(query['lum_percentile_lower'])),
            abs(float(query['lum_val']) - float(query['lum_percentile_upper'])))

        self.luminosity = ufloat(float(query['lum_val']),l_err)

