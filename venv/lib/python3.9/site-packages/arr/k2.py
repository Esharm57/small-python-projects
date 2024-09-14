import everest
from astroquery.vizier import Vizier
import astropy.units as u
import everest
import lightkurve as lk
import matplotlib.pyplot as pl
from matplotlib.axes import Axes

from arr.simbad import Simbad

class K2:
    def __init__(self, target : Simbad,target_name : str):
        v = Vizier(columns=['ID', 'Teff', 'Kpmag', '[Fe/H]', 'E(B-V)', 'logg', 'Rad'])

        try:
            kic_entry = v.query_region(target.coord,radius=1*u.arcsecond,catalog='IV/34/epic')[0]
        except IndexError:
            self.kic_id = None
            self.t_eff = None
            self.kepmag = None
            self.log_g = None
            self.fe_h = None
            self.e_b_v = None
            self.radius = None
            self.lc = None
            return

        self.kic_id = kic_entry['ID'][0]
        self.t_eff = float(kic_entry['Teff'][0])*u.K
        self.kepmag = float(kic_entry['Kpmag'][0])*u.mag
        self.log_g = float(kic_entry['logg'][0])
        self.fe_h =float(kic_entry['__Fe_H_'][0])
        self.e_b_v = float(kic_entry['E_B-V_'][0])
        self.radius = float(kic_entry['Rad'][0])*u.solRad

        star = everest.Everest(self.kic_id)
        self.lc = lk.LightCurve(time=star.time[~star.mask],flux=star.fcor[~star.mask])

    def plot(self, show=False, **kwargs):
        for i in ['color', 'ylabel', 'normalize']:
            try:
                del kwargs[i]
            except KeyError:
                pass

        ax: Axes = self.lc.scatter(color='k', normalize=True, **kwargs)

        if show:
            pl.show()
        else:
            return ax

    @property
    def observed(self):
        return self.kic_id is not None