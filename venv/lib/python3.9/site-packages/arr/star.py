from arr.gaia import Gaia
from arr.tess import Tess
from arr.simbad import Simbad
from arr.kepler import Kepler
from arr.k2 import K2
from arr.reference import Reference
import astropy.units as u
from texttable import Texttable
from astropy.coordinates import SkyCoord

from warnings import warn

class Star:
    def __init__(self,target_name,coordinates : SkyCoord = None):
        self.target_name = target_name
        try:
            self.simbad = Simbad(target_name,coordinates)
        except TypeError:
            raise ValueError(f"Can't resolve {target_name}.")

        self.gaia = Gaia(self.simbad.coord)
        self.tess = Tess(self.simbad,target_name)
        if self.tess.observed and f"TIC {self.tess.tic_id}" not in self.simbad.id_list:
            self.simbad.id_list += [f"TIC {self.tess.tic_id}"]

        self.kepler = Kepler(self.simbad,target_name)
        if self.kepler.observed and f"KIC {self.kepler.kic_id}" not in self.simbad.id_list:
            self.simbad.id_list += [f"KIC {self.kepler.kic_id}"]

        self.k2 = K2(self.simbad,target_name)
        if self.k2.observed and f"EPIC {self.k2.kic_id}" not in self.simbad.id_list:
            self.simbad.id_list += [f"EPIC {self.k2.kic_id}"]

    @property
    def coord(self):
        return self.gaia.coord

    @property
    def spectral_type(self):
        return self.simbad.spectral_type

    @property
    def bibliography(self):
        for bib in self.simbad.bibliography:
            try:
                r = Reference(bib)
                print(f"{r.title}\n{','.join(r.authors)}\nPublication date: {r.pubdate}\n\n{r.abstract}\n\n")
                i = ""
                while i not in ['s','o','a']:
                    i = input("Enter action: (s)kip, (o)pen, '(a)rxiv'\n")

                if i == 'o':
                    r.show()
                elif i=='a':
                    r.arxiv()
            except KeyboardInterrupt:
                break


        return self.simbad.bibliography

    def plot(self,show = False,**kwargs):
        if self.kepler.observed:
            self.kepler.plot(show,**kwargs)
        elif self.tess.observed:
            self.tess.plot(show,**kwargs)
        elif self.k2.observed:
            self.k2.plot(show,**kwargs)
        else:
            warn("No photometric observations available.",UserWarning)

    @property
    def lc(self):
        if self.tess is not None:
            return self.tess.lc
        else:
            warn("No TESS observations available.",UserWarning)

    def info(self):
        simbad_table = Texttable()

        simbad_table.add_rows([
            ['ID',self.simbad.id],
            ['Type',self.simbad.type],
            ['Spectral type',self.simbad.spectral_type],
            ['Temperature',self.simbad.atmosphere.t_eff],
            ['log(g)',self.simbad.atmosphere.log_g],
            ['Fe_H',self.simbad.atmosphere.fe_h],
            ['U_mag', self.simbad.u.value],
            ['B_mag', self.simbad.b.value],
            ['V_mag', self.simbad.v.value],
            ['R_mag', self.simbad.r.value],
            ['I_mag', self.simbad.i.value],
            ['G_mag', self.simbad.g.value],
            ['J_mag', self.simbad.j.value],
            ['H_mag', self.simbad.h.value],
            ['K_mag', self.simbad.k.value],
        ])

        name_table = Texttable()

        name_table.add_rows([[
            'Other names',"\n".join(self.simbad.id_list)
        ]])

        text = f"Simbad:\n{simbad_table.draw()}\n\nNames:\n{name_table.draw()}"
        print(text)






