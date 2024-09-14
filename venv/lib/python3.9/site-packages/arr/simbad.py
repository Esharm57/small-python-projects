from astroquery.simbad import Simbad as aq_simbad
from astropy.coordinates import SkyCoord
import webbrowser

aq_simbad.ROW_LIMIT = -1
import astropy.units as u

from arr.reference import Reference

sim = aq_simbad()
sim.add_votable_fields(
    'otype(V)'
    , 'ids'
    , 'biblio'
    , 'fe_h'
    , 'membership'
    , 'plx'
    , 'pm'
    , 'sp'
    , 'sp_bibcode'
    , 'sp_qual'
    , 'ubv'
    , 'flux(U)'
    , 'flux_bibcode(U)'
    , 'flux(B)'
    , 'flux_bibcode(B)'
    , 'flux(V)'
    , 'flux_bibcode(V)'
    , 'flux(R)'
    , 'flux_bibcode(R)'
    , 'flux(I)'
    , 'flux_bibcode(I)'
    , 'flux(G)'
    , 'flux_bibcode(G)'
    , 'flux(J)'
    , 'flux_bibcode(J)'
    , 'flux(H)'
    , 'flux_bibcode(H)'
    , 'flux(K)'
    , 'flux_bibcode(K)'
)
flux_types = {
    'u': ('FLUX_U', 'FLUX_BIBCODE_U'),
    'b': ('FLUX_B', 'FLUX_BIBCODE_B'),
    'v': ('FLUX_V', 'FLUX_BIBCODE_V'),
    'r': ('FLUX_R', 'FLUX_BIBCODE_R'),
    'i': ('FLUX_I', 'FLUX_BIBCODE_I'),
    'g': ('FLUX_G', 'FLUX_BIBCODE_G'),
    'j': ('FLUX_J', 'FLUX_BIBCODE_J'),
    'h': ('FLUX_H', 'FLUX_BIBCODE_H'),
    'k': ('FLUX_K', 'FLUX_BIBCODE_K')
}


class Flux:
    def __init__(self, name, value, bibcode):
        self.name = name
        try:
            self.value = float(value)*u.mag
        except:
            self.value = None

        try:
            self.ref = Reference(bibcode)
        except:
            self.ref = None


class Atmosphere:
    def __init__(self, t_eff, log_g, fe_h, bib_code):
        try:
            self.t_eff = float(t_eff) * u.K
        except:
            self.t_eff = None

        try:
            self.log_g = float(log_g) * u.dex
        except:
            self.log_g = None

        try:
            self.fe_h = float(fe_h)
        except:
            self.fe_h = None

        try:
            self.ref = Reference(bib_code)
        except:
            self.ref = None


class Simbad:
    def __init__(self, target_name: str,coordinates : SkyCoord = None):
        if coordinates is not None:
            res = sim.query_region(coordinates,radius=2*u.arcminute)
            self.coord = coordinates
        else:
            res = sim.query_object(target_name)
            self.coord = SkyCoord(res['RA'][0] + " " + res['DEC'][0], unit=(u.hourangle, u.deg))

        for name, (value, bibcode) in flux_types.items():
            self.__dict__[name] = Flux(name, res[value][0], res[bibcode][0])

        self.type = res['OTYPE_V'][0].decode()
        self.bibliography = res['BIBLIO'][0].decode().split("|")
        self.id = res['MAIN_ID'][0].decode()
        self.id_list = res['IDS'][0].decode().split("|")

        self.atmosphere = Atmosphere(res['Fe_H_Teff'], res['Fe_H_log_g'], res['Fe_H_Fe_H'], res['Fe_H_bibcode'][0])

        self.spectral_type = res['SP_TYPE'][0].decode()
        self.spectral_type_ref = Reference(res['SP_BIBCODE'][0])
        self.target_name = target_name

    @property
    def ra(self):
        return self.coord.ra

    @property
    def dec(self):
        return self.coord.dec

    def get_ref(self,index : int):
        try:
            return Reference(self.bibliography[index])
        except:
            return None

    def open(self):
        webbrowser.open("http://simbad.u-strasbg.fr/simbad/sim-id?Ident="+self.target_name.replace(" ","+"), new=2)
